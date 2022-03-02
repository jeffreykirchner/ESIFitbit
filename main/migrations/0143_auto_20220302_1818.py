# Generated by Django 3.2.12 on 2022-03-02 18:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0142_auto_20220228_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_day',
            name='survey_link',
            field=models.CharField(default='', max_length=1000, verbose_name='Survey Link'),
        ),
        migrations.AddField(
            model_name='session_day',
            name='survey_required',
            field=models.BooleanField(default=False, verbose_name='Survey Complete'),
        ),
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='activity_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Subject Activity Key'),
        ),
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='survey_complete',
            field=models.BooleanField(default=True, verbose_name='Survey Complete'),
        ),
    ]
