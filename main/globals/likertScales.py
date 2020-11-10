
from django.db import models
from django.utils.translation import gettext_lazy as _

class Likert_importance(models.TextChoices):
    DEFAULT = "", _('')
    ZERO = 0, _('N/A')
    ONE = 1, _('Very Unimportant')
    TWO = 2, _('Unimportant')
    THREE = 3, _('Somewhat Unimportant')
    FOUR = 4, _('Neutral')
    FIVE = 5, _('Somewhat Important')
    SIX = 6, _('Important')
    SEVEN = 7, _('Very Important')

class Likert_satisfaction(models.TextChoices):
    DEFAULT = "", _('')
    ZERO = 0, _('N/A')
    ONE = 1, _('Very Unsatisfied')
    TWO = 2, _('Unsatisfied')
    THREE = 3, _('Somewhat Unsatisfied')
    FOUR = 4, _('Neutral')
    FIVE = 5, _('Somewhat Satisfied')
    SIX = 6, _('Satisfied')
    SEVEN = 7, _('Very Satisfied')

class Likert_variation(models.TextChoices):
    DEFAULT = "", _('')
    ZERO = 0, _('N/A')
    ONE = 1, _('No two nights are the same')
    TWO = 2, _('Very much variation')
    THREE = 3, _('Much variation')
    FOUR = 4, _('Average amount of variation')
    FIVE = 5, _('Little variation')
    SIX = 6, _('Very little variation')
    SEVEN = 7, _('No variation')

class Likert_variation2(models.TextChoices):
    DEFAULT = "", _('')
    ZERO = 0, _('N/A')
    ONE = 1, _('No two days are the same')
    TWO = 2, _('Very much variation')
    THREE = 3, _('Much variation')
    FOUR = 4, _('Average amount of variation')
    FIVE = 5, _('Little variation')
    SIX = 6, _('Very little variation')
    SEVEN = 7, _('No variation')