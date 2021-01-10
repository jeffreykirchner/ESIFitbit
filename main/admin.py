from django.contrib import admin
from django.conf import settings
from django.db.models.functions import Lower

from main.forms import Parameters_form,Consent_form_form

from main.models import *

# Register your models here.

admin.site.site_header = settings.ADMIN_SITE_HEADER

#global parameters
class parametersadmin(admin.ModelAdmin):
      def has_add_permission(self, request, obj=None):
            return False
      
      def has_delete_permission(self, request, obj=None):
            return False
      
      form = Parameters_form

      actions = []

admin.site.register(Parameters, parametersadmin)

#consent forms
class consent_formsadmin(admin.ModelAdmin):

      ordering = [Lower('name')]

      actions = []
      list_display = ['name']
      
      form = Consent_form_form

      

admin.site.register(Consent_forms, consent_formsadmin)
