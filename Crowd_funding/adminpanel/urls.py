from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    #-------------------Login sections-------------------

    path('',views.admin_login,name='admin_login'),
    path('admin_login_check',views.admin_login_check,name='admin_login_check'),
    path('logout/',views.Logout,name='logout'),

    #---------------Change password-------------------

    path('password',views.password,name='password'),
    path('change_pass',views.change_pass,name='change_pass'),

    #---------------------home section---------------

    path('index/',views.index,name='admin_index'),

    #---------------------------user view-----------------
    
    path('user/',views.user,name='user'),

    #---------------------------wallet management-----------------
    
    path('wallet/',views.wallet_management,name='wallet'),

    #--------------------charity_category section----------------

    path('charity_category/',views.charity_category, name="charity_category"),
    path('charity_category_save/',views.charity_category_save,name='charity_category_save'),
    path('delete_charity_category/<int:pk>/',views.delete_charity_category,name='delete_charity_category'),

    #------------------add charity section------------------

    path('charities/',views.charities,name="charities"),
    path('charity_save/',views.charity_save,name="charity_save"),

    #----------------------view charity section----------------------

    path('view_charity/',views.view_charity,name="view_charity"),  
    path('delete_charity/<int:pk>/',views.delete_charity,name="delete_charity"),



    #--------------------campaign_category section----------------

    path('campaign_category/',views.campaign_category, name="campaign_category"),
    path('campaign_category_save/',views.campaign_category_save,name='campaign_category_save'),
    path('delete_campaign_category/<int:pk>/',views.delete_campaign_category,name='delete_campaign_category'),

    #-------------------add campaign section------------------

    path('campaign/',views.campaign,name="campaign"),
    path('campaign_save/',views.campaign_save,name="campaign_save"),

    #----------------------view campaign section----------------------

    path('view_campaign/',views.view_campaign,name="view_campaign"),  
    path('delete_campaign/<int:pk>/',views.delete_campaign,name="delete_campaign"),

  
    
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
