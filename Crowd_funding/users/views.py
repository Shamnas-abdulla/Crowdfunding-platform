from django.shortcuts import render,redirect
from adminpanel.models import user_signup as signup,OTP
from adminpanel.models import addCharity, addCampaign,Wallet,Charity_Category,Campaign_Category
from adminpanel.models import SetAmountCharity,SetAmountCampaign,Autodeduct
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm,YourLoginForm
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
import pyotp
from datetime import datetime,timedelta,date
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
#current date
today = datetime.now()
#date limit for charity listing in auto deduction
date_limit = today + timedelta(days=60)

#============================auto deduction method=====================================
def autoDeduct():
     charity = SetAmountCharity.objects.all()
     campaign = SetAmountCampaign.objects.all()
     users = set() #for storing users present in auto deduction
     for charity_instances in charity:
          if charity_instances.name_id not in users:
              users.add(charity_instances.name_id)
     
     for campaign_instances in campaign:
          if campaign_instances.name_id not in users:
              users.add(campaign_instances.name_id)
 
     print(users)
     #Iterating users
     for user_instances in users:
          flag = False
          charities = SetAmountCharity.objects.filter(name_id=user_instances).all()
          campaigns = SetAmountCampaign.objects.filter(name_id=user_instances).all()
          total_amount = Autodeduct.objects.filter(name_id=user_instances).values('total_amt').first()['total_amt']
          wallet = Wallet.objects.filter(user_id=user_instances).first()
 
          if wallet is not None and total_amount <= wallet.amount:
               if charities:
                   #iterating selected charities
                   for charity_instance in charities:
                         amount = charity_instance.amount 
                         charity_id = charity_instance.charity_name_id
     
                         add_charity_instance = addCharity.objects.filter(id=charity_id).first() 
                         if add_charity_instance is not None and add_charity_instance.amount >= amount:
                             add_charity_instance.amount -= amount #deduct amount from charity
                             add_charity_instance.save()
                             
                             wallet.amount -= amount # deduct amount from user wallet
                             wallet.save()
   
               if campaigns:
                   #Iterating selected campaigns
                    for campaign_instance in campaigns:
                         amount = campaign_instance.amount 
                         campaign_id = campaign_instance.campaign_name_id 
     
                         add_campaign_instance = addCampaign.objects.filter(id=campaign_id).first() 
                         if add_campaign_instance is not None and add_campaign_instance.amount >= amount:
                             add_campaign_instance.amount -= amount # deduct amount from campaign
                             add_campaign_instance.save()
                             
                             wallet.amount -= amount # deduct amount from user wallet
                             wallet.save()
    
          else:
              flag = True #If the user does not have enough funds in their wallet to make a auto deduction, the flag is set to true
 
          print(flag)
          #if  flag == True send email to user to inform monthly deduction is not completed
          if flag:
              subject = "From Crowd funding"
              message = f'''Hi,{wallet.user.name}
            Your monthly deduction is not completed
            because of a lack of amount in your wallet.
              '''
              email_from = settings.EMAIL_HOST_USER
              recipient_list = [wallet.user.email, ]
              send_mail(subject, message, email_from, recipient_list)
          #if   flag == False send email to user to inform monthly deduction is successfully completed
          else:
              subject = "From Crowd funding"
              message = f'''Hi,{wallet.user.name}
              Your monthly deduction has been successfully completed.
       Thank you for your donation. Please note that, in some cases,
       deductions may not be completed for specific charities or campaigns due to the
       total amount allocated for those charities or campaigns being exceeded
              '''
              email_from = settings.EMAIL_HOST_USER
              recipient_list = [wallet.user.email, ]
              send_mail(subject, message, email_from, recipient_list)

     for delete_charity in charity:
          if delete_charity.charity_name.amount <= 0 or delete_charity.amount > delete_charity.charity_name.amount:
              # Delete charity from SetAmountCharity if the charity amount is <= 0 or set amount is greater than charity amount
                  delete_charity.delete()
                 
          
     for delete_campaign in campaign:
              if delete_campaign.campaign_name.amount <= 0 or delete_campaign.amount > delete_campaign.campaign_name.amount:
                  # Delete campaign from SetAmountCampaign if the campaign amount is <= 0 or set amount is greater than campaign amount
                    delete_campaign.delete()
                    
     
          

          
          
#=================================total_money_deduct================================
# Method to find total amount is deduct from wallet to all charities and campaigns in auto deduction
def total_money_deduct():
    users = signup.objects.all()  
    Autodeduct.objects.all().delete() # Delete existing data's present in Autodeduct model
    #iterate users
    for user in users:
        user_id = user.id
        charity_instances = SetAmountCharity.objects.filter(name_id=user_id)
        campaign_instances = SetAmountCampaign.objects.filter(name_id=user_id)

        total = 0  

        for deduct_instance in charity_instances:
            total += deduct_instance.amount # Sum of all charity amount present in the SetAmountCharity 
        for deduct_instance in campaign_instances:
             total += deduct_instance.amount # Sum of all campaign amount present in the SetAmountCampaign
        #Add user and total amount in Autodeduct model
        assign_total = Autodeduct.objects.create(
             name_id = user_id,
             total_amt = total
        )
        assign_total.save()

     
#=================================generate_email====================================
#Email generation If the user does not have enough funds in their wallet to make a auto deduction 
def generate_email():
    total_money_list = Autodeduct.objects.all()
    
    for total_money in total_money_list:
        print(total_money.total_amt)
        
        if total_money.total_amt != 0:
            user_id = total_money.name
            
            try:
                user_wallet = Wallet.objects.get(user_id=user_id)
                
                if user_wallet.amount < total_money.total_amt:
                    subject = "From Crowd funding"
                    message = f'''Hi {user_id.name},.
                    Kindly be informed that your wallet lacks sufficient funds for
                    tomorrow's scheduled auto monthly deduction
                    We encourage you to top up your wallet with the necessary amount.
                    The amount you need to pay monthly deduction is : {total_money.total_amt} .
                    '''
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user_id.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                else:
                    pass #Sufficient amount in user wallet.
                    
            except Wallet.DoesNotExist:
                print("No wallet found for the user.")







# call these two function in 28'th day of every month
# To inform there is no enough amount in their wallet to auto deduction  
if datetime.today().day == 2:
     total_money_deduct()
     generate_email()

# Call these functions in 1'st day of every month for auto deduction
if datetime.today().day == 1:
     total_money_deduct()
     autoDeduct()
     




#================================index page===========================================
def index(request):
    charity = addCharity.objects.order_by('end_date').filter(end_date__gte = today,amount__gt = 0)[0:4]
    campaign = addCampaign.objects.order_by('end_date').filter(end_date__gte = today,amount__gt = 0)[0:4]
    context = {
         'charity':charity,
         'campaign':campaign,
    }
    return render(request,"users/index.html",context)

#===========================Information page=================================
def ReadMore(request):
     return render(request,"users/ReadMore.html")

#==============================list_charity============================================
def list_Charity(request):
     today = datetime.now().date()
     data = addCharity.objects.filter(end_date__gte= today,amount__gt = 0)
     categories = Charity_Category.objects.all()
     cat_id = request.GET.get('categories')
     if cat_id:
          data = addCharity.objects.filter(end_date__gte= today,amount__gt = 0,category_id=cat_id)
     else:
          data = addCharity.objects.filter(end_date__gte= today,amount__gt = 0)
     context = {'data':data,
                'categories':categories}
     return render(request,"users/list_charity.html",context)

#==============================list_campaign=========================================
def list_Campaign(request):
     today = datetime.now().date()
     data = addCampaign.objects.filter(end_date__gte= today,amount__gt = 0)
     categories = Campaign_Category.objects.all()
     cat_id = request.GET.get('categories')
     if cat_id:
          data = addCampaign.objects.filter(end_date__gte= today,amount__gt = 0,category_id=cat_id)
     else:
          data = addCampaign.objects.filter(end_date__gte= today,amount__gt = 0)
     context = {'data':data,
                'categories':categories}
     return render(request,"users/list_campaign.html",context)
 

#==================================SIGN_IN====================================

@csrf_protect
def sign_in(request):
    if request.method == 'POST':
        form = YourLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                 return redirect(request.POST.get('next'))
            else:  
                return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = YourLoginForm()

    return render(request, 'users/login.html', {'form': form})


#==================================SIGN_UP=============================================
@csrf_protect
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Successfully signed up.')
            return redirect('signin')
        else:
            pass
    else:
        form = UserSignupForm()

    return render(request, 'users/signup.html', {'form': form})





#===============================LOGOUT=======================================
@login_required
def logout_view(request):
    if request.user.is_authenticated:
         logout(request)
         return redirect('signin')
    # Redirect to a specific page after logout, or you can customize this as needed.
    return redirect('signin') 




#===============================WALLET PAGE=================================
@login_required
def create_wallet(request):
    print("User authenticated:", request.user.is_authenticated)
    if request.user.is_authenticated:
        user_id = request.user.id
        wallet = Wallet.objects.filter(user_id=user_id).first()

        if wallet is None:
            new_wallet = Wallet.objects.create(user_id=user_id, amount=0)
            new_wallet.save()

        user = request.user.username

        wallet = Wallet.objects.filter(user_id=user_id).first()
        charities = addCharity.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
        campaigns = addCampaign.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
        set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id=user_id).all()
        set_campaign_list = [data.campaign_name_id for data in set_amount_campaign_list]

        set_amount_charity_list = SetAmountCharity.objects.filter(name_id=user_id).all()
        set_charity_list = [data.charity_name_id for data in set_amount_charity_list]

        set_amount_campaign = SetAmountCampaign.objects.all().filter(name_id=user_id)
        set_amount_charity = SetAmountCharity.objects.all().filter(name_id=user_id)

        context = {
            'user': user,
            'amount': wallet.amount,
            'charities': charities,
            'campaigns': campaigns,
            'set_amount_campaign': set_amount_campaign,
            'set_amount_charity': set_amount_charity,
            'set_campaign_list': set_campaign_list,
            'set_charity_list': set_charity_list,
        }

        return render(request, "users/create_wallet.html", context)
    else:
        messages.info(request, 'Please log in to access your wallet.')
        return redirect('signin')





#============================ADD AMOUNT TO WALLET==================================
@login_required
def Add_amount(request):
    print(f"User authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print("User is authenticated.")
        zero_error = ''
        user = request.user.id
        user_name = request.user.username
        wallet = Wallet.objects.filter(user_id=user).first()
        amount = wallet.amount
        
        charities = addCharity.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
        campaigns = addCampaign.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
        set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id=user).all()
        set_campaign_list = [data.campaign_name_id for data in set_amount_campaign_list]

        set_amount_charity_list = SetAmountCharity.objects.filter(name_id=user).all()
        set_charity_list = [data.charity_name_id for data in set_amount_charity_list]

        set_amount_campaign = SetAmountCampaign.objects.all().filter(name_id=user)
        set_amount_charity = SetAmountCharity.objects.all().filter(name_id=user)

        context = {
            'user': user_name,
            'amount': amount,
            'set_amount_charity': set_amount_charity,
            'set_amount_campaign': set_amount_campaign,
            'charities': charities,
            'campaigns': campaigns,
            'set_campaign_list': set_campaign_list,
            'set_charity_list': set_charity_list,
        }

        if request.method == 'POST':
            print("POST request received.")
            amount_str = request.POST.get('amount', '')
            print(f"Amount from POST: {amount_str}")

            if amount_str.isdigit() and int(amount_str) > 0 and amount_str is not None:
                amounts = int(amount_str)
                print(f"Valid amount: {amounts}")

                if wallet:
                    old_amount = wallet.amount
                    total_amount = int(amounts) + old_amount
                    wallet.amount = total_amount
                    wallet.save()
                    context.update({'amount': total_amount})
                    print("Wallet updated.")
                    return render(request, "users/create_wallet.html", context)
                else:
                    wallet = Wallet(user_id=user, amount=amounts)
                    wallet.save()
                    context.update({'amount': amounts})
                    print("New wallet created.")
                    return render(request, "users/create_wallet.html", context)
            else:
                zero_error = "Please enter a valid positive amount "
                context.update({'zero_error': zero_error})
                print("Invalid amount entered.")
                return render(request, "users/create_wallet.html", context)
        else:
            print("GET request received.")
            return render(request, "users/create_wallet.html", context)
    else:
        print("User is not authenticated. Redirecting to login page.")
        return render(request, "users/login.html")
 


#========================DONATE TO CHARITY PAGE=================================  
from django.http import HttpResponseRedirect  
def donate_charity(request,donate_id):
    if request.user.is_authenticated:
        data = addCharity.objects.filter(id=donate_id).first()
        return render(request,'users/donateCharity.html',{'data':data})
    else:
        return HttpResponseRedirect(redirect('signin').url + f"?next={request.path}")
        
            

     

#====================CHARITY DONATTION COMPLETION============================
def charity_cmplt(request,donate_id):
     
     if request.user.is_authenticated:
          data = addCharity.objects.filter(id=donate_id).first()
          no_money_error = ''
          money_limit_error = ''
          if request.method == 'POST':   
               user = request.user.id

               amount_str = request.POST.get('amount', '')

               if amount_str.isdigit() and int(amount_str) > 0 and amount_str != None:
                    amounts = int(amount_str)
                    print(amounts)
                    charity = addCharity.objects.filter(id=donate_id).first()
                    wallet = Wallet.objects.filter(user_id=user).first()
                    if wallet.amount >= amounts and charity.amount >= amounts:
                         charity.amount -= amounts
                         charity.save()
                         wallet.amount -= amounts
                         wallet.save()
                         succes = "Thanks for your donation"
                         set_charity = SetAmountCharity.objects.filter(charity_name_id=donate_id).all()
                         if charity.amount <= 0:
                              set_charity.delete()

                         return render(request,'users/donateCharity.html',{'data':data,'success':succes})
                    else :
                         if wallet.amount < amounts:
                              no_money_error = "No enough amount in your wallet"
                         elif charity.amount < amounts:
                              money_limit_error = "Charity amount limit is passed "
                         context = {
                                   'no_money_error':no_money_error,
                                   'money_limit_error':money_limit_error,
                                   'data':data
                                   }
     
                         return render(request,'users/donateCharity.html',context)
               else:     
                     zero_error = "Please enter a valid positive amount "
                     return render(request, 'users/donateCharity.html', {'zero_error': zero_error, 'data': data})
     else:
          return redirect('signin')

          
          
     


#========================DONATE TO CAMPAIGN PAGE================================= 
def donate_campaign(request,donate_id):
     if request.user.is_authenticated:
          data = addCampaign.objects.filter(id=donate_id).first()
          return render(request,'users/donateCampaign.html',{'data':data})
     else:
        return HttpResponseRedirect(redirect('signin').url + f"?next={request.path}")

#====================CHARITY DONATTION COMPLETION============================    
def campaign_cmplt(request, donate_id):
    if request.user.is_authenticated:
        data = addCampaign.objects.filter(id=donate_id).first()
        no_money_error = ''
        money_limit_error = ''
        zero_error = ''

        if request.method == 'POST':
            user = request.user.id
            amount_str = request.POST.get('amount', '')

            if amount_str.isdigit() and int(amount_str) > 0 and amount_str != None:
                amounts = int(amount_str)
                print(amounts)

                campaign = addCampaign.objects.filter(id=donate_id).first()
                wallet = Wallet.objects.filter(user_id=user).first()

                if wallet.amount >= amounts and campaign.amount >= amounts:
                    campaign.amount -= amounts
                    campaign.save()
                    wallet.amount -= amounts
                    wallet.save()
                    success = "Thanks for your donation"
                    set_campaign = SetAmountCampaign.objects.filter(campaign_name_id=donate_id).all()
                    if campaign.amount <= 0:
                         set_campaign.delete()
                    return render(request, 'users/donateCampaign.html', {'data': data, 'success': success})
                else:
                    if campaign.amount < amounts:
                        money_limit_error = "Charity amount limit is passed "
                    elif wallet.amount < amounts:
                        no_money_error = "No enough amount in your wallet"

                    context = {
                        'no_money_error': no_money_error,
                        'money_limit_error': money_limit_error,
                        'data': data,
                    }
                    return render(request, 'users/donateCampaign.html', context)
            else:
                zero_error = "Please enter a valid positive amount "
                return render(request, 'users/donateCampaign.html', {'zero_error': zero_error, 'data': data})

    return render(request, 'user/index.html')



#==============================SET CHARITY FOR AUTO DEDUCTION===========================
def set_Charity(request,charity_id):
     if request.user.is_authenticated:
          user = request.user.id
          user_name = request.user.username
          charity = addCharity.objects.all().filter(id=charity_id).first()
          wallet = Wallet.objects.filter(user_id = user).first()
          charities = addCharity.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
          campaigns = addCampaign.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
          set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id=user).all()
          set_campaign_list = [data.campaign_name_id for data in set_amount_campaign_list]
  
          set_amount_charity_list = SetAmountCharity.objects.filter(name_id=user).all()
          set_charity_list = [data.charity_name_id for data in set_amount_charity_list]
  
          set_amount_campaign = SetAmountCampaign.objects.all().filter(name_id=user)
          set_amount_charity = SetAmountCharity.objects.all().filter(name_id=user)

          context = {
             'user':user_name,
             'amount':wallet.amount,
             'charities':charities,
             'campaigns':campaigns,
             'set_amount_charity':set_amount_charity,
             'set_amount_campaign':set_amount_campaign,
             'set_campaign_list':set_campaign_list,
             'set_charity_list':set_charity_list,
             
             }
          

          if request.method == 'POST':
               amount_str = request.POST.get('set_amount', '')
               charity_amount = addCharity.objects.filter(id=charity_id).values('amount').first()['amount']

               if amount_str.isdigit() and int(amount_str) > 0 and amount_str != None and int(amount_str) <= charity_amount:
                    amount = int(amount_str)
                    print(amount)
                    if SetAmountCharity.objects.all().filter(name_id=user,charity_name_id=charity_id):
                         
                         set_amount = SetAmountCharity.objects.all().filter(name_id=user,charity_name_id=charity_id).first()
                         set_amount.amount = amount
                         set_amount.save()
                         
                    else:
                         
                         set_amount = SetAmountCharity.objects.create(
                         name_id= user,
                         charity_name_id = charity_id,
                         amount = amount,
                         end_date = charity.end_date,
                         )
                         set_amount.save()
                         set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id =user).all()
                         set_campaign_list = []
                         set_campaign_list.clear()
                         for data in set_amount_campaign_list:
                              set_campaign_list.append(data.campaign_name_id)
                          
                         set_amount_charity_list = SetAmountCharity.objects.filter(name_id = user).all()
                         set_charity_list = []
                         set_charity_list.clear()
                         for data in set_amount_charity_list:
                              set_charity_list.append(data.charity_name_id)
                         context.update({'set_campaign_list':set_campaign_list,'set_charity_list':set_charity_list,})
                    
                    return render(request,'users/create_wallet.html',context)
               else:
                    zero_error_charity = "Please enter a valid positive amount "
                    context.update({'zero_error_charity':zero_error_charity})
                    return render(request, 'users/create_wallet.html',context)            
          else:

               return render(request,'users/create_wallet.html',context)
     else:
          return redirect("signin")

#==============================SET CHARITY FOR AUTO DEDUCTION===========================        
def set_Campaign(request,campaign_id):
     if request.user.is_authenticated:
          
          user = request.user.id
          user_name = request.user.username
          
          wallet = Wallet.objects.filter(user_id = user).first()
          charities = addCharity.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
          campaigns = addCampaign.objects.all().filter(end_date__gte=date.today(), amount__gt=0)
          set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id=user).all()
          set_campaign_list = [data.campaign_name_id for data in set_amount_campaign_list]
  
          set_amount_charity_list = SetAmountCharity.objects.filter(name_id=user).all()
          set_charity_list = [data.charity_name_id for data in set_amount_charity_list]
  
          set_amount_campaign = SetAmountCampaign.objects.all().filter(name_id=user)
          set_amount_charity = SetAmountCharity.objects.all().filter(name_id=user)
          
          
          context = {
             'user':user_name,
             'charities':charities,
             'amount':wallet.amount,
             'campaigns':campaigns,
             'set_amount_campaign':set_amount_campaign,
             'set_amount_charity':set_amount_charity,
             'set_campaign_list':set_campaign_list,'set_charity_list':set_charity_list,
             
             
             }
          if request.method == 'POST':
               charity = addCampaign.objects.all().filter(id=campaign_id).first()
               amount_str = request.POST.get('set_amount', '')
               campaign_amount = addCampaign.objects.filter(id=campaign_id).values('amount').first()['amount']

               if amount_str.isdigit() and int(amount_str) > 0 and amount_str != None and int(amount_str) <= campaign_amount:
                    amount = int(amount_str)
                    print(amount)
               
                    if SetAmountCampaign.objects.all().filter(name_id=user,campaign_name_id=campaign_id):
                         amount = int(request.POST.get('set_amount'))
                         set_amount = SetAmountCampaign.objects.all().filter(name_id=user,campaign_name_id=campaign_id).first()
                         set_amount.amount = amount
                         set_amount.save()
                         
                    else:
                         amount = int(request.POST.get('set_amount'))
                         
                         set_amount = SetAmountCampaign.objects.create(
                         name_id= user,
                         campaign_name_id = campaign_id,
                         amount = amount,
                         end_date = charity.end_date,
                         )
                         set_amount.save()
                         set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id=user).all()
                         set_campaign_list = []
                         set_campaign_list.clear()
                         for data in set_amount_campaign_list:
                              set_campaign_list.append(data.campaign_name_id)
                         
                         set_amount_charity_list = SetAmountCharity.objects.filter(name_id=user).all()
                         set_charity_list = []
                         set_charity_list.clear()
                         for data in set_amount_charity_list:
                              set_charity_list.append(data.charity_name_id)
                                   
                                     
                         context.update({'set_campaign_list':set_campaign_list,'set_charity_list':set_charity_list,})
                                   
                    return render(request,'users/create_wallet.html',context)
               else:
                    zero_error_campaign = "Please enter a valid positive amount "
                    context.update({'zero_error_campaign':zero_error_campaign})
                    return render(request, 'users/create_wallet.html',context) 
          else:
               return render(request,'users/create_wallet.html')
     else:
          return redirect("signin")

#==================DELETE SETTED CHARITY FOR AUTO DEDUCTION==================================
def delete_set_charity(request,charity_id):
     if request.user.is_authenticated:
          user = request.user.id
          data = SetAmountCharity.objects.filter(charity_name_id=charity_id).all()
          data.delete()  
          set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id = user).all()
          set_campaign_list = []
          set_campaign_list.clear()
          for data in set_amount_campaign_list:
               set_campaign_list.append(data.campaign_name_id)
          
          set_amount_charity_list = SetAmountCharity.objects.filter(name_id = user).all()
          set_charity_list = []
          set_campaign_list.clear()
          for data in set_amount_charity_list:
               set_charity_list.append(data.charity_name_id)
  
          return redirect('create_wallet')      
     

#==================DELETE SETTED CAMPAIGN FOR AUTO DEDUCTION==================================
def delete_set_campaign(request,campaign_id):
     if request.user.is_authenticated:
          user = request.user.id
          
          data = SetAmountCampaign.objects.filter(campaign_name_id=campaign_id).all()
          data.delete()  
          set_amount_campaign_list = SetAmountCampaign.objects.filter(name_id = user).all()
          set_campaign_list = []
          set_campaign_list.clear()
          for data in set_amount_campaign_list:
               set_campaign_list.append(data.campaign_name_id)
          
          set_amount_charity_list = SetAmountCharity.objects.filter(name_id=user).all()
          set_charity_list = []
          set_charity_list.clear()
          for data in set_amount_charity_list:
               set_charity_list.append(data.charity_name_id)
          
          return redirect('create_wallet')   
     

#==========================FORGOT PASSWORD SECTION==============================
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_data = signup.objects.values('id', 'email').get(email=email)
        except signup.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('forgot_password')

        # Generate OTP secret
        otp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(otp_secret, digits=6)
        current_otp = totp.now()
        

        OTP.objects.create(user=str(user_data['id']), otp_secret=current_otp)

        email_param = user_data.get('email', '')
        send_otp_email(email_param, current_otp)
        url = reverse('verify_otp', args=[email_param])
        return redirect(url)

    return render(request, 'users/registration/forgot_password.html')

def verify_otp(request, email):  
    print(f"{email} is received")
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '')
        user = signup.objects.values('id', 'email').get(email=email)
        user_id = str(user['id'])
        
        otp_instance = OTP.objects.filter(user=user_id).last()

        if otp_instance and otp_entered == otp_instance.otp_secret:
            # OTP verification successful
            email_param = user.get('email', '')
            url = reverse('reset_password', args=[email_param])
            return redirect(url)
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'users/registration/verify_otp.html')

def reset_password(request, email):
    if request.method == 'POST':
        try:
            user = signup.objects.get(email=email)
        except signup.DoesNotExist:
            messages.error(request, f"User with email '{email}' does not exist.")
            return render(request, 'users/registration/reset_password.html')

        new_password = request.POST.get('new_password')

        # Validate the new password
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return render(request, 'users/registration/reset_password.html')

        # Update user's password
        user.set_password(new_password)
        user.save()

        # Clear OTP data
        OTP.objects.filter(user=user).delete()

        messages.success(request, 'Password reset successfully. You can now log in.')
        return redirect('signin')

    return render(request, 'users/registration/reset_password.html')



def send_otp_email(email, otp_secret):
    subject = 'Your OTP for Password Reset'
    message = f'Your OTP is: {otp_secret}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
