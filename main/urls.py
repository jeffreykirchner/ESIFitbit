from django.contrib import admin
from django.urls import path,re_path
from django.views.generic.base import RedirectView
from django.conf.urls import include,url
from django.conf import settings
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

urlpatterns = [
    #admin site
    re_path(r'^admin/login/$', RedirectView.as_view(url=settings.LOGIN_URL, permanent=True, query_string=True)),    

    #account control
    path('',views.Home,name='home'),                 #direct user by subject type
    path('accounts/', include('django.contrib.auth.urls')),  #django built in account registrations
       
    #staff
    path('staffHome/',views.Staff_Home,name='staff_home'),
    path('session/<id>/',views.Staff_Session,name='staff_session'),

    #subject
    path('subjectHome/',views.Home,name='home2'),
    path('subjectHome/<uuid:id>/',csrf_exempt(views.Subject_Home),name='subject_home'),

    #test page
    #path('test/',TemplateView.as_view(template_name="test.html"),name='test'),
   
    #fitbit
    path('fitBit/',views.fitBit,name='fitBit'),
    
]