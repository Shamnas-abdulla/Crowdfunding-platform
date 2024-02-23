from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import AddCampaign, CampaignCategoryForm, CharityCategoryForm,AddCharity
from .models import Campaign_Category, Charity_Category, addCampaign , admin_Login,addCharity,user_signup,Wallet
from datetime import date
from django.contrib.auth.hashers import make_password,check_password


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
        if user:
               
                   
                     request.session['name'] = user.user_name
                     request.session['id'] = user.id
                     return render(request,'adminpanel/index.html') 
               
                     
       
            
        else:
               return render(request,'adminpanel/login.html',{'error':'invalid username or password'})
    else:

        return render(request,'adminpanel/login.html')   


def Logout(request):
     your_data = request.session.get('id', None)
     if your_data is not None:
        del request.session['id']
     logout(request)
     return render(request,'adminpanel/login.html')

#-------------------Change password----------------

def password(request):
     if request.session.get('id'):
      
           return render(request,'adminpanel/password.html')
     else:
         return render(request,'adminpanel/login.html')
         

def change_pass(request):
     id = request.session['id'] 
     if request.method == 'POST':
        password = request.POST.get('password')
        admin_Login.objects.filter(id=id).update(password=password)
        return render(request,'adminpanel/password.html')
        
        

#----------------------index page-------------------------------------


def index(request):

    if request.session.get('id'):
        return render(request,"adminpanel/index.html")
    else:
        return render(request,'adminpanel/login.html')
      #checking login do this all page    


#-----------------------users view-------------------------------------


def user(request):
    if request.session.get('id'):
        users = user_signup.objects.all()
        return render(request,'adminpanel/users.html',{'users':users})
    else:
        return render(request,'adminpanel/login.html')
  


#-----------------------users view-------------------------------------


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
      
        if addCampaign.objects.filter(name=char_name).exists():
             context = {'form': form,'error': 'Category name already exist'}
             return render(request, 'adminpanel/charities.html',context)
        if addCampaign.objects.filter(email=email).exists():
             context = {'form': form,'error': 'Email already exist'}
             return render(request, 'adminpanel/charities.html',context)
        if addCampaign.objects.filter(phone=phone).exists():
            context = {'form': form,'error': 'Phone already exist'}
            return render(request, 'adminpanel/charities.html',context)
        if form.is_valid():
            form.save()     
            context = {'form': form,'msg': 'Charity is saved'}
            return render(request, 'adminpanel/charities.html', context)
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
    form = AddCampaign()
    return render(request, 'adminpanel/campaign.html',{'form': form})



def campaign_save(request):
    if request.method == "POST":
        form = AddCampaign(request.POST, request.FILES)#edited by ranya
        comp_name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
      
        if addCampaign.objects.filter(name=comp_name).exists():#edted by Ranya
             context = {'form': form,'error': 'Campaign name already exist'}
             return render(request, 'adminpanel/campaign.html',context)
        if addCampaign.objects.filter(email=email).exists():#do this for mobile
             context = {'form': form,'error': 'Email already exist'}
             return render(request, 'adminpanel/campaign.html',context)
        if addCampaign.objects.filter(phone=phone).exists():#do this for mobile
            context = {'form': form,'error': 'Phone already exist'}
            return render(request, 'adminpanel/campaign.html',context)
        if form.is_valid():
            form.save()     
            context = {'form': form,'msg': 'Campaign is saved'}
            return render(request, 'adminpanel/campaign.html', context)
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
    charity = addCharity.objects.get(pk=pk)
    charity.delete()
    return redirect('view_campaign')