
from django.db import models
from django.utils.translation import gettext_lazy as _

class Likert_importance(models.TextChoices):
    ONE = 1, _('Very Unimportant')
    TWO = 2, _('Unimportant')
    THREE = 3, _('Somewhat Unimportant')
    FOUR = 4, _('Neutral')
    FIVE = 5, _('Somewhat Important')
    SIX = 6, _('Important')
    SEVEN = 7, _('Very Important')

class Likert_satisfaction(models.TextChoices):
    ONE = 1, _('Very Unsatisfied')
    TWO = 2, _('Unsatisfied')
    THREE = 3, _('Somewhat Unsatisfied')
    FOUR = 4, _('Neutral')
    FIVE = 5, _('Somewhat Satisfied')
    SIX = 6, _('Satisfied')
    SEVEN = 7, _('Very Satisfied')

class Likert_variation(models.TextChoices):
    ONE = 1, _('Very High')
    TWO = 2, _('High')
    THREE = 3, _('Somewhat High')
    FOUR = 4, _('Average')
    FIVE = 5, _('Somewhat Low')
    SIX = 6, _('Low')
    SEVEN = 7, _('Very Low')