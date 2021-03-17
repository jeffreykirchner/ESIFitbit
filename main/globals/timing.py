'''
choices for session timing
'''
from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeBlock(models.TextChoices):
    '''
    time blocks
    '''
    ONE = 'ONE', _('ONE')
    TWO = "TWO", _('TWO')
    THREE = "THREE", _('THREE')

class PageType(models.TextChoices):
    '''
    page tabs
    '''
    HEART = 'HEART', _('HEART')
    SLEEP = "SLEEP", _('SLEEP')
    PAY = "PAY", _('PAY')

class NoticeType(models.TextChoices):
    '''
    Time block change notice types
    '''
    ADVANCE = 'ADVANCE', _('ADVANCE')
    START = "START", _('START')
