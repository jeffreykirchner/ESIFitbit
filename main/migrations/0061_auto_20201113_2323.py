# Generated by Django 3.1.2 on 2020-11-13 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0060_auto_20201113_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='cancelation_text',
            field=models.CharField(default='', max_length=10000),
        ),
        migrations.AddField(
            model_name='session',
            name='cancelation_text_subject',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
