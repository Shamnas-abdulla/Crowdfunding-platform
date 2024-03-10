from django.urls import path
from . import views


#urls
urlpatterns = [
    #=====================index=====================
    path('',views.index,name='index'),
    
    #==================Information=================
    path('ReadMore',views.ReadMore,name='ReadMore'),

    #=====================signup=====================
    path('signup/', views.user_signup, name="user_signup"),

    #=====================signin======================
    path('signin/', views.sign_in, name='signin'),

    #=======================logout===================
    path('logout_user/', views.logout_view, name='logout_user'),
    
    #================Forgot password section======================
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),

    #==================Listing charity and campaign======================
    path('list_charity/',views.list_Charity,name='list_charity'),
    path('list_campaign/',views.list_Campaign,name='list_campaign'),

    #====================Donating charity and campaign====================
    path('donate_charity/<int:donate_id>/',views.donate_charity,name="donate_charity"),
    path('charity_cmplt/<int:donate_id>/',views.charity_cmplt,name="charity_cmplt"),
    path('donate_campaign/<int:donate_id>/',views.donate_campaign,name="donate_campaign"),
    path('campaign_cmplt/<int:donate_id>/',views.campaign_cmplt,name="campaign_cmplt"),
    
    #========================Wallet Section==============================
    path('create_wallet/',views.create_wallet,name="create_wallet"),
    path('Add_amt/',views.Add_amount,name="Add_amt"),

    path('search_charity/', views.search_charity, name='search_charity'),
    path('search_campaign/', views.search_campaign, name='search_campaign'),

    #======================Auto deduct Section=========================
    path('set_charity/<int:charity_id>',views.set_Charity,name="set_charity"),
    path('set_campaign/<int:campaign_id>',views.set_Campaign,name="set_campaign"),
    path('delete_set_charity/<int:charity_id>',views.delete_set_charity,name="delete_set_charity"),
    path('delete_set_campaign/<int:campaign_id>',views.delete_set_campaign,name="delete_set_campaign"),

    
]



   


