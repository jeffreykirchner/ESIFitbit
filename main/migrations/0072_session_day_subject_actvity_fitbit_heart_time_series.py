# Generated by Django 3.1.2 on 2020-12-03 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0071_auto_20201203_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_day_subject_actvity',
            name='fitbit_heart_time_series',
            field=models.CharField(default='', max_length=100000),
        ),
    ]