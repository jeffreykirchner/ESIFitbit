# Generated by Django 3.1.4 on 2021-03-01 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0096_session_day_subject_actvity_fitbit_immune_time_series'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['-start_date'], 'verbose_name': 'Experiment Session', 'verbose_name_plural': 'Experiment Sessions'},
        ),
        migrations.AddField(
            model_name='session',
            name='allow_delete',
            field=models.BooleanField(default=True),
        ),
    ]
