from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import AddCampaign, CampaignCategoryForm, CharityCategoryForm,AddCharity
from .models import Campaign_Category, Charity_Category, addCampaign , admin_Login,addCharity,user_signup,Wallet,OTP,AdminOTP
from datetime import date
from django.contrib.auth.hashers import make_password,check_password
import pyotp
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError



    


#---------------------Admin login section--------------------------


def admin_login(request):
    return render(request,"adminpanel/login.html")


def admin_login_check(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        try:
            user =  admin_Login.objects.filter(user_name=user_name,password=password).get()
            
        except admin_Login.DoesNotExist:
                user= None
                messages.error(request, 'invalid username or password')
        if user:
             request.session['name'] = user.user_name
             request.session['id'] = user.id
             return render(request,'adminpanel/index.html')    
        else:
               
               return render(request,'adminpanel/login.html')
    else:
        messages.error(request, 'invalid username or password')

        return render(request,'adminpanel/login.html')   


def Logout(request):
     your_data = request.session.get('id', None)
     if your_data is not None:
        del request.session['id']
        logout(request)
        return render(request,'adminpanel/login.html')



         

        
#-----------------------Add new admin-------------------------
def addAdmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username or email already exists
        if admin_Login.objects.filter(user_name=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
        elif admin_Login.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please choose a different one.')
        else:
            # If username and email are unique, create a new admin
            admin_Login.objects.create(user_name=username, email=email, password=password)
            messages.success(request, 'New admin added successfully.')
            return redirect('AddAdmin')  # Redirect to the same page after successful form submission
    return render(request, 'adminpanel/AddAdmin.html')
#----------------------index page-------------------------------------



def index(request):

    if request.session.get('id'):
        return render(request,"adminpanel/index.html")
    else:
        return render(request,'adminpanel/login.html')
      #checking login do this all page    



#-----------------------Admin view-------------------------------------
from django.shortcuts import get_object_or_404

def adminView(request):
    if request.session.get('id'):
        admin_id = request.session.get('id')
        logged_admin = get_object_or_404(admin_Login, id=admin_id)
        logged_admin_user_name = logged_admin.user_name
        admins = admin_Login.objects.all()
        context = {
        'admins': admins,
        'can_remove': logged_admin_user_name == "shamnas",
    }
        return render(request,'adminpanel/Admin.html',context)
    else:
        return render(request,'adminpanel/Admin.html')
    
def deleteAdmin(request,pk):
    if request.session.get('id'):
        admin = admin_Login.objects.get(pk=pk)
        admin.delete()
        return redirect('adminView')
    else:
        return render(request,'adminpanel/login.html')

  
#-----------------------users view-------------------------------------


def user(request):
    if request.session.get('id'):
        users = user_signup.objects.all()
        return render(request,'adminpanel/users.html',{'users':users})
    else:
        return render(request,'adminpanel/login.html')
  


#-----------------------Wallet view-------------------------------------


def wallet_management(request):
    if request.session.get('id'):
        data = Wallet.objects.all()
        return render(request,'adminpanel/wallet.html',{'data':data})
    else:
        return render(request,'adminpanel/login.html')
    
#----------------------charity category------------------------


def charity_category(request):
    if request.session.get('id'):
        category_lists = Charity_Category.objects.all()  
        return render(request,"adminpanel/charity_category.html",{'lists':category_lists})
    else:
        return render(request,'adminpanel/login.html')
    



def charity_category_save(request):
    if request.method == "POST":
        form = CharityCategoryForm(request.POST)
        category_lists = Charity_Category.objects.all()
        if form.is_valid():
            data = form['name'].value()   
            if Charity_Category.objects.filter(name = data).exists():
                    context = {'form': form,'error': 'This category Exist','lists':category_lists}
                    return render(request, 'adminpanel\charity_category.html',context)


            form.save()
           
            category_lists = Charity_Category.objects.all()  
            return render(request,"adminpanel/charity_category.html",{'lists':category_lists})
        else:
           
            context = {'form': form,'error': 'Please enter category','lists':category_lists}
            return render(request, 'adminpanel\charity_category.html',context)


    else:
        form = CharityCategoryForm()

    return render(request, 'adminpanel\charity_category.html',{'form': form,'lists':category_lists})

def delete_charity_category(request,pk):
    if request.session.get('id'):
        charity = Charity_Category.objects.get(pk=pk)
        charity.delete()
        return redirect('charity_category')
    else:
        return render(request,'adminpanel/login.html')
    



#--------------------------------Add charity------------------------


def charities(request):
    if request.session.get('id'):
        form = AddCharity()
        return render(request, 'adminpanel/charities.html',{'form': form})
    else:
        return render(request,'adminpanel/login.html')
    



def charity_save(request):
    if request.method == "POST":
        form = AddCharity(request.POST, request.FILES)
        char_name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
      
        if addCharity.objects.filter(email=email).exists():
             context = {'form': form,'error': 'Email already exist'}
             return render(request, 'adminpanel/charities.html',context)
        if addCharity.objects.filter(phone=phone).exists():
            context = {'form': form,'error': 'Phone already exist'}
            return render(request, 'adminpanel/charities.html',context)
        if form.is_valid():
                new_charity = form.save()
                charity_id = new_charity.id

                # Construct the donation link
                donation_link = f"http://127.0.0.1:8000/donate_charity/{charity_id}/"
                msg = "Charity is saved"

                return render(request, 'adminpanel/charities.html', {'donation_link': donation_link,'form':form,'msg':msg})
        else:
            context = {'form': form,'error': 'Please enter valid details'}
            return render(request, 'adminpanel/charities.html',context)


    
    form = AddCharity()
    return render(request, 'adminpanel\charities.html',{'form': form})



#---------------------------View charity---------------------------


def view_charity(request):
    if request.session.get('id'):
        today = date.today()
        print(today)
        data = addCharity.objects.all()
        return render(request,"adminpanel/View charity.html",{'data':data,'today':today})
    else:
        return render(request,'adminpanel/login.html')
    

def delete_charity(request,pk):
    charity = addCharity.objects.get(pk=pk)
    charity.delete()
    return redirect('view_charity')



#----------------------campaign category------------------------


def campaign_category(request):
    if request.session.get('id'):
        category_lists = Campaign_Category.objects.all()  
        return render(request,"adminpanel/campaign_category.html",{'lists':category_lists})
    else:
        return render(request,'adminpanel/login.html')
    



def campaign_category_save(request):
    if request.method == "POST":
        form = CampaignCategoryForm(request.POST)
        category_lists = Campaign_Category.objects.all()
        if form.is_valid():
            data = form['name'].value()   
            if Campaign_Category.objects.filter(name = data).exists():
                    context = {'form': form,'error': 'This category Exist','lists':category_lists}
                    return render(request, 'adminpanel\campaign_category.html',context)


            form.save()
            context = {'form': form,'msg': 'Category is saved','lists':category_lists}
            return render(request, 'adminpanel/campaign_category.html', context)
        else:
            context = {'form': form,'error': 'Please enter category','lists':category_lists}
            return render(request, 'adminpanel/campaign_category.html',context)


    else:
        form = CampaignCategoryForm()

    return render(request, 'adminpanel/campaign_category.html',{'form': form,'lists':category_lists})


def delete_campaign_category(request,pk):
    charity = Campaign_Category.objects.get(pk=pk)
    charity.delete()
    return redirect('campaign_category')
  


#--------------------------------Add campaign------------------------


def campaign(request):
    if request.session.get('id'):
        form = AddCampaign()
        return render(request, 'adminpanel/campaign.html',{'form': form})
    else:
        return render(request,'adminpanel/login.html')
    



def campaign_save(request):
    if request.method == "POST":
        form = AddCampaign(request.POST, request.FILES)#edited by ranya
        comp_name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
      
        if addCampaign.objects.filter(email=email).exists():#do this for mobile
             context = {'form': form,'error': 'Email already exist'}
             return render(request, 'adminpanel/campaign.html',context)
        if addCampaign.objects.filter(phone=phone).exists():#do this for mobile
            context = {'form': form,'error': 'Phone already exist'}
            return render(request, 'adminpanel/campaign.html',context)
        if form.is_valid():
                new_campaign = form.save()
                campaign_id = new_campaign.id

                # Construct the donation link
                donation_link = f"http://127.0.0.1:8000/donate_campaign/{campaign_id}/"
                msg = "Campaign is saved"

                return render(request, 'adminpanel/campaign.html', {'donation_link': donation_link,'form':form,'msg':msg})
        else:
            errors = form.errors
            context = {'form': form,'error': errors}
            return render(request, 'adminpanel/campaign.html',context)


    
    form = AddCampaign()
    return render(request, 'adminpanel/campaign.html',{'form': form})



#---------------------------View campaign---------------------------


def view_campaign(request):
    if request.session.get('id'):
       today = date.today()
       print(today)
       data = addCampaign.objects.all()
       return render(request,"adminpanel/View campaign.html",{'data':data,'today':today})
    else:
        return render(request,'adminpanel/login.html')


def delete_campaign(request,pk):
    charity = addCampaign.objects.get(pk=pk)
    charity.delete()
    return redirect('view_campaign')


#==========================FORGOT PASSWORD SECTION==============================
def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_data = admin_Login.objects.values('id', 'email').get(email=email)
        except admin_Login.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('ForgotPassword')

        # Generate OTP secret
        otp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(otp_secret, digits=6)
        current_otp = totp.now()
        

        AdminOTP.objects.create(user=str(user_data['id']), otp_secret=current_otp)

        email_param = user_data.get('email', '')
        send_otp_email(email_param, current_otp)
        url = reverse('VerifyOtp', args=[email_param])
        return redirect(url)

    return render(request, 'adminpanel/registration/ForgotPassword.html')

def VerifyOtp(request, email):  
    print(f"{email} is received")
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '')
        user = admin_Login.objects.values('id', 'email').get(email=email)
        user_id = str(user['id'])
        
        otp_instance = AdminOTP.objects.filter(user=user_id).last()

        if otp_instance and otp_entered == otp_instance.otp_secret:
            # OTP verification successful
            email_param = user.get('email', '')
            url = reverse('ResetPassword', args=[email_param])
            return redirect(url)
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'adminpanel/registration/VerifyOtp.html')

def ResetPassword(request, email):
    if request.method == 'POST':
        try:
            user = admin_Login.objects.get(email=email)
        except admin_Login.DoesNotExist:
            messages.error(request, f"User with email '{email}' does not exist.")
            return render(request, 'adminpanel/registration/ResetPassword.html')
        

        new_password = request.POST.get('new_password')

        # Validate the new password
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return render(request, 'adminpanel/registration/ResetPassword.html')

        # Update user's password
        admin_Login.objects.filter(email=email).update(password=new_password)
        

        # Clear OTP data
        AdminOTP.objects.filter(user=user).delete()

        messages.success(request, 'Password reset successfully. You can now log in.')
        return redirect('admin_login')

    return render(request, 'adminpanel/registration/ResetPassword.html')



def send_otp_email(email, otp_secret):
    subject = 'Your OTP for Password Reset'
    message = f'Your OTP is: {otp_secret}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
