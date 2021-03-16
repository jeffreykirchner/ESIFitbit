'''
instruction set page
'''

from django.db import models

from main.models import InstructionSet
from main.globals import TimeBlock, PageType

class InstructionSetPage(models.Model):
    '''
    instruction set page
    '''

    instruction_set = models.ForeignKey(InstructionSet, on_delete=models.CASCADE, related_name="instruction_set_pages")

    time_block = models.CharField(max_length=100, choices=TimeBlock.choices)          #which time block page should be shown in       
    page_type = models.CharField(max_length=100, choices=PageType.choices)            #which page tab to show on  

    text = models.CharField(verbose_name="Text", max_length = 50000,default = "")     #text of instructions

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'Time Block {self.time_block} Tab {self.page_type}'
    
    class Meta:
        verbose_name = 'Session Instuction Set Page'
        verbose_name_plural = 'Session Instuction Set Pages'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['instruction_set', 'time_block', 'page_type'], name='unique_instruction_page'),
        ]

    def json(self):
        '''
        return json object of model
        '''

        return {
            'id' : self.id,
            'time_block' : self.time_block,
            'page_type' : self.page_type,
            'text' : self.text,
        }