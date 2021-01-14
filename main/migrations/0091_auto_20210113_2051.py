# Generated by Django 3.1.4 on 2021-01-13 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0090_parameters_testemailaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='blockChangeSubject',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='parameters',
            name='blockPreChangeSubject',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='parameters',
            name='blockPreChangeText',
            field=models.CharField(default='', max_length=5000),
        ),
    ]