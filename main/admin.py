from django.contrib import admin
from django.conf import settings

from main.forms import Parameters_form

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
