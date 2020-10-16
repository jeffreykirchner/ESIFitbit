from django.contrib import admin
from django.urls import path,re_path
from django.views.generic.base import RedirectView
from django.conf.urls import include,url
from django.conf import settings
from . import views

urlpatterns = [
    #admin site
    re_path(r'^admin/login/$', RedirectView.as_view(url=settings.LOGIN_URL, permanent=True, query_string=True)),    

    #account control
    path('',views.Home,name='home'),                 #direct user by subject type
    path('accounts/', include('django.contrib.auth.urls')),  #django built in account registrations
    # path('profile/', views.updateProfile,name='profile'),    #custom profile 
    # path('accounts/profile/', views.updateProfile,name='profile'), #custom profile         
    # path('profileCreate/',views.profileCreate,name='profileCreate'),
    # path('profileVerify/<token>/',views.profileVerify,name='profileVerify'),
    # path('profileVerifyResend/',views.profileVerifyResend,name='profileVerifyResend'),
    
    #staff
    path('staffHome/',views.Staff_Home,name='staff_home'),

    #subject
    path('subjectHome/',views.Subject_Home,name='subject_home'),
    
]