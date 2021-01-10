from django.db import models


#consent forms available for subjects
class Consent_forms(models.Model):
    
    name = models.CharField(verbose_name="Name", max_length = 1000,default = "")           #Name of consent form
    body_text = models.CharField(verbose_name="Text", max_length = 50000,default = "")     #text of consent form

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Consent Form'
        verbose_name_plural = 'Consent Forms'
    
    def json(self):
        return{
            "name":self.name,
            "body_text":self.body_text,
        }