# Generated by Django 3.2 on 2021-04-30 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0129_session_auto_pay'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['-start_date', 'title'], 'verbose_name': 'Experiment Session', 'verbose_name_plural': 'Experiment Sessions'},
        ),
    ]