from django.contrib import admin
from django.conf import settings
from django.db.models.functions import Lower
from django.utils.translation import ngettext
from django.contrib import messages

from main.forms import Parameters_form, Consent_form_form, SessionFormAdmin, InstructionSetPageForm

from main.models import *

# Register your models here.

admin.site.site_header = settings.ADMIN_SITE_HEADER

#global parameters
class Parametersadmin(admin.ModelAdmin):
      '''
      parameters admin screen
      '''
      def has_add_permission(self, request, obj=None):
            return False

      def has_delete_permission(self, request, obj=None):
            return False

      form = Parameters_form

      actions = []

admin.site.register(Parameters, Parametersadmin)

#consent forms
class consent_formsadmin(admin.ModelAdmin):

      ordering = [Lower('name')]

      actions = []
      list_display = ['name']
      
      form = Consent_form_form      

admin.site.register(Consent_forms, consent_formsadmin)

#session form
class SessionAdmin(admin.ModelAdmin):

      ordering = ['-start_date']

      actions = []
      list_display = ['title','start_date','soft_delete']
      
      form = SessionFormAdmin   

admin.site.register(Session, SessionAdmin)

class SessionDaysAdmin(admin.ModelAdmin):
      def has_add_permission(self, request, obj=None):
            return False
      
      def has_delete_permission(self, request, obj=None):
            return False
            
      ordering = ['session__title','period_number']

      list_display = ['__title__','id','date','period_number','payments_sent']

      search_fields = ['session__title','id','period_number','date','payments_sent']

      readonly_fields = ('period_number','date','payments_sent','session')
admin.site.register(Session_day,SessionDaysAdmin)

#instruction set page
class InstructionSetPageInline(admin.TabularInline):
      '''
      instruction set page admin screen
      '''
      def has_delete_permission(self, request, obj=None):
            return False
      
      def has_add_permission(self, request, obj=None):
            return False

      form = InstructionSetPageForm
      model = InstructionSetPage

#Instruction set
class InstructionSetAdmin(admin.ModelAdmin):
      '''
      instruction set admin screen
      '''
      def setup_pages(self, request, queryset):
            '''
            setup blank instrution pages
            '''
            setup_list=[]

            for i_set in queryset:
                  setup_list.append(i_set.setup())

            self.message_user(request, ngettext(
                  '%d instruction set was setup.',
                  '%d instruction sets were setup.',
                  len(setup_list),
            ) % len(setup_list), messages.SUCCESS)
      setup_pages.short_description = "Setup new pages"

      def duplicate_set(self, request, queryset):
            '''
            duplicate instruction set
            '''
            if queryset.count() != 1:
                  self.message_user(request,"Select only one instruction set to copy.", messages.ERROR)
                  return

            base_instruction_set = queryset.first()

            instruction_set = InstructionSet()
            instruction_set.save()
            instruction_set.setup()
            instruction_set.copy_pages(base_instruction_set)

            self.message_user(request,f'{base_instruction_set} has been duplicated', messages.SUCCESS)
      duplicate_set.short_description = "Duplicate Instruction Set"

      inlines = [
        InstructionSetPageInline,
      ]
      actions = [setup_pages, duplicate_set]

admin.site.register(InstructionSet, InstructionSetAdmin)




# admin.site.register(InstructionSetPage, InstructionSetPageAdmin)

