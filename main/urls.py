'''
main url patterns
'''
from django.urls import path,re_path
from django.views.generic.base import RedirectView
from django.conf.urls import include, url
from django.conf import settings
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #admin site
    re_path(r'^admin/login/$', RedirectView.as_view(url=settings.LOGIN_URL, permanent=True, query_string=True)),    

    #account control
    path('',views.Home,name='home'),                         #direct user by subject type
    path('accounts/', include('django.contrib.auth.urls')),  #django built in account registrations
       
    #staff
    path('staffHome/',views.Staff_Home,name='staff_home'),
    path('session/<id>/',views.Staff_Session,name='staff_session'),
    path('adminFunctions/',views.Admin_functions,name='admin_functions'),

    #subject
    path('subjectHome/',views.Home,name='home2'),
    path('subjectHome/<uuid:id>/',csrf_exempt(views.Subject_Home),name='subject_home'),

    #icons
    path('favicon.ico',RedirectView.as_view(url='/static/favicon.ico'),name='favicon'),
    path('apple-touch-icon-precomposed.png',RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'),name='favicon'),
    path('apple-touch-icon.png',RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'),name='favicon'),
    path('apple-touch-icon-120x120-precomposed.png',RedirectView.as_view(url='/static/apple-touch-icon-precomposed.png'),name='favicon'),

    #test page
    #path('test/',TemplateView.as_view(template_name="test.html"),name='test'),
   
    #fitbit
    path('fitBit/',views.fitBit,name='fitBit'),

    #crong
    path('runCrons/', views.RunCronsView.as_view(), name='runCrons')
    
]