# Generated by Django 3.1.2 on 2020-10-19 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20201018_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameterset',
            name='number_of_players',
        ),
    ]
