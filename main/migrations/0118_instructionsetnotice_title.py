# Generated by Django 3.1.7 on 2021-03-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0117_auto_20210316_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionsetnotice',
            name='title',
            field=models.CharField(default='', max_length=500, verbose_name='Text'),
        ),
    ]