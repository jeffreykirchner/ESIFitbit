# Generated by Django 3.2.12 on 2022-02-28 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0139_alter_consent_forms_body_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='fitbit_birthday',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='fitbit_weight',
            field=models.IntegerField(default=0),
        ),
    ]
