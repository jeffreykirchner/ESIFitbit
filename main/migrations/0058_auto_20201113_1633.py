# Generated by Django 3.1.2 on 2020-11-13 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_auto_20201113_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session_day_subject_actvity',
            name='heart_activity_minutes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='session_day_subject_actvity',
            name='immune_activity_minutes',
            field=models.IntegerField(default=0),
        ),
    ]