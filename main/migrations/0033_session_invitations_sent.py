# Generated by Django 3.1.2 on 2020-11-02 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_session_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='invitations_sent',
            field=models.BooleanField(default=False),
        ),
    ]
