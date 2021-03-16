'''
reusable instruction set for sessions
'''
import logging

from django.db import models
from django.db.models import Q

import main.models

from main.globals import TimeBlock, PageType


class InstructionSet(models.Model):
    '''
    instruction set model
    '''

    title = models.CharField(max_length = 300, default="*** Title Here ***")    #name of instruction set

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Session Instuction Set'
        verbose_name_plural = 'Session Instuction Sets'
        ordering = ['title']

    def setup(self):
        '''
        setup new instruction set
        '''

        #check that not already setup
        if self.instruction_set_pages.count() > 0:
            return
        
        #add instruction pages
        for t_b in TimeBlock.choices:
            for p_t in PageType.choices:
                new_page = main.models.InstructionSetPage(instruction_set=self, time_block=t_b[0], page_type=p_t[0])
                new_page.save()
    
    def get_page_text(self, time_block, page_type):
        '''
        get specified page text
        '''
        logger = logging.getLogger(__name__)
        logger.info(f'get_page_text {time_block} {page_type}')

        return self.instruction_set_pages.get(Q(time_block = time_block) & Q(page_type = page_type)).text

    def copy_pages(self, i_set):
        '''
        copy instruction pages
        '''

        for page in self.instruction_set_pages.all():
            page.text = i_set.get_page_text(page.time_block, page.page_type)
            page.save()
    
    def json(self):
        '''
        return json object of model
        '''

        return {
            "id" : self.id,
            "title" : self.title,
        }
        

       
