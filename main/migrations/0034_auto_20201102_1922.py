# Generated by Django 3.1.2 on 2020-11-02 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_session_invitations_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='invitationTextSubject',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='session',
            name='invitation_text',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
