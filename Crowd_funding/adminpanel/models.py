from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _



#--------------------Admin login -------------------------
class admin_Login(models.Model):
    user_name = models.CharField(max_length=100,null=False)
    password = models.CharField(max_length=50,null=False)



#-------------------Charity category----------------------

class Charity_Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
#-----------------------Add charity----------------------

class addCharity(models.Model):
    name = models.CharField(max_length=100)
    founder_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254,null=True,unique = True)
    phone = models.CharField(max_length=10,null=True)
    category = models.ForeignKey("Charity_Category", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    end_date = models.DateField()
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    
   

#--------------------Campaign category---------------------

class Campaign_Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

#-------------------------Add campaign------------------

class addCampaign(models.Model):
    name = models.CharField(max_length=100)
    founder_name = models.CharField(max_length=100)#edited by ranya (make migration and migrate)
    email = models.EmailField(max_length=254,unique=True)
    phone = models.CharField(max_length=10,unique=True)
    category = models.ForeignKey("Campaign_Category", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    end_date = models.DateField()
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
   


#--------------------User signup ----------------------
class user_signup(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=10)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set_groups',  # Change to a unique name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set_permissions',  # Change to a unique name
    )


    



    

#===============================Wallet=============================
class Wallet(models.Model):
    user = models.ForeignKey("user_signup", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    mandatory = False


#=====================Auto deduct models==========================

class SetAmountCharity(models.Model):
    name = models.ForeignKey(user_signup, on_delete=models.CASCADE,default='')
    charity_name = models.ForeignKey(addCharity, on_delete=models.CASCADE,default='',null=True)
    amount  = models.IntegerField() 
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class SetAmountCampaign(models.Model):
    name = models.ForeignKey(user_signup, on_delete=models.CASCADE,default='')
    campaign_name = models.ForeignKey(addCampaign, on_delete=models.CASCADE,default='')
    amount  = models.IntegerField() 
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Autodeduct(models.Model):
    name = models.ForeignKey(user_signup, on_delete=models.CASCADE)
    total_amt = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)



#======================OTP============================
    
class OTP(models.Model):
    user = models.CharField(max_length=255)
    otp_secret = models.CharField(max_length=32)
    otp_created_at = models.DateTimeField(auto_now_add=True)
  

    def __str__(self):
        return str(self.user) 

    
