# Generated by Django 3.2.12 on 2022-02-21 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0130_alter_session_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameterset',
            name='show_group',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parameterset',
            name='sleep_tracking',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='auto_pay',
            field=models.BooleanField(default=False),
        ),
    ]