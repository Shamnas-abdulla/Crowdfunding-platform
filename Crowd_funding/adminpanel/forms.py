from django import forms
from .models import Campaign_Category, Charity_Category, addCampaign,admin_Login,addCharity
from django.forms.widgets import NumberInput


#----------------------Charity category form--------------------

class CharityCategoryForm(forms.ModelForm):
    class Meta:
        model = Charity_Category
        fields = ['name'] 



#-----------------------Add charity form--------------------

class AddCharity(forms.ModelForm):
    class Meta:
        model = addCharity
        fields = ['name','founder_name','email','phone','category','amount','end_date','description' ,'image',
                  ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Charity name'}),
            'founder_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Founder name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone number'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control','placeholder':'Total amount'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'End date', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'accept': '.jpg, .png, .gif,.jpeg'}),
            'description': forms.Textarea(attrs={'class':'md-textarea form-control','placeholder':'Description'}),
            
        }
        labels = {
            'name': 'Charity Name',
            'founder_name': 'Founder Name',
            'email': 'Email',
            'phone': 'Phone Number',
            'category': 'Category',
            'amount': 'Total Amount',
            'end_date': 'End Date',
            'image': 'Image',
            'description': 'Description',
        }




#----------------------Campaign category form--------------------

class CampaignCategoryForm(forms.ModelForm):
    class Meta:
        model = Campaign_Category
        fields = ['name'] 


        

#-----------------------Add campaign form--------------------

class AddCampaign(forms.ModelForm):
    class Meta:
        model = addCampaign
        fields = ['name','founder_name','email','phone','category','amount','end_date','description' ,'image',
                  ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Campaign name'}),
            'founder_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Founder name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone number'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control','placeholder':'Total amount'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'End date', 'class': 'form-control'}),
             'image': forms.FileInput(attrs={'accept': '.jpg, .png, .gif,.jpeg'}),
            'description': forms.Textarea(attrs={'class':'md-textarea form-control','placeholder':'Description'}),
           
        }
        labels = {
            'name': 'Charity Name',
            'founder_name': 'Founder Name',
            'email': 'Email',
            'phone': 'Phone Number',
            'category': 'Category',
            'amount': 'Total Amount',
            'end_date': 'End Date',
            'image': 'Image',
            'description': 'Description',
        }


    