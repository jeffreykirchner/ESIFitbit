# Generated by Django 3.1.2 on 2020-11-07 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_parameters_trackerdataonly'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='consentFormRequired',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='session_subject',
            name='consent_form',
            field=models.BooleanField(default=False),
        ),
    ]
