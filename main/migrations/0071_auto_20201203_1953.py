# Generated by Django 3.1.2 on 2020-12-03 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0070_auto_20201203_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='fitbit_minutes_heart_cardio',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='fitbit_minutes_heart_fat_burn',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='fitbit_minutes_heart_out_of_range',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='fitbit_minutes_heart_peak',
            field=models.IntegerField(default=0),
        ),
    ]
