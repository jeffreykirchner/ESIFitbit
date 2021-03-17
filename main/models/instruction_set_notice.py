'''
instruction set page
'''

from django.db import models

from main.models import InstructionSet
from main.globals import TimeBlock, NoticeType

class InstructionSetNotice(models.Model):
    '''
    instruction set page
    '''

    instruction_set = models.ForeignKey(InstructionSet, on_delete=models.CASCADE, related_name="instruction_set_notices")

    time_block = models.CharField(max_length=100, choices=TimeBlock.choices)            #which time block page should be shown in       
    notice_type = models.CharField(max_length=100, choices=NoticeType.choices)          #which page tab to show on  

    title = models.CharField(verbose_name="Title", max_length = 500,default = "")            #header text of notice
    text = models.CharField(verbose_name="Page Text", max_length = 50000,default = "")       #text of instructions

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'Time Block {self.time_block} Notice {self.notice_type}'
    
    class Meta:
        verbose_name = 'Session Instuction Set Notice'
        verbose_name_plural = 'Session Instuction Set Notices'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['instruction_set', 'time_block', 'notice_type'], name='unique_instruction_notice'),
        ]

    def json(self):
        '''
        return json object of model
        '''

        return {
            'id' : self.id,
            'time_block' : self.time_block,
            'notice_type' : self.notice_type,
            'text' : self.text,
        }