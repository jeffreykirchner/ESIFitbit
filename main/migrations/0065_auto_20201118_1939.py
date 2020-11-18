# Generated by Django 3.1.2 on 2020-11-18 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0064_parameters_manualhelptext'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_subject',
            name='display_color',
            field=models.CharField(default='#FFFFFF', max_length=300, verbose_name='Graph Color'),
        ),
        migrations.AlterField(
            model_name='session_subject',
            name='consent_required',
            field=models.BooleanField(default=True, verbose_name='Consent Form Signed'),
        ),
        migrations.AlterField(
            model_name='session_subject',
            name='consent_signature',
            field=models.CharField(default='', max_length=300, verbose_name='Consent Form Signature'),
        ),
        migrations.AlterField(
            model_name='session_subject',
            name='id_number',
            field=models.IntegerField(null=True, verbose_name='ID Number in Session'),
        ),
        migrations.AlterField(
            model_name='session_subject',
            name='questionnaire1_required',
            field=models.BooleanField(default=True, verbose_name='Pre-questionnaire Complete'),
        ),
        migrations.AlterField(
            model_name='session_subject',
            name='questionnaire2_required',
            field=models.BooleanField(default=True, verbose_name='Post-questionnaire Complete'),
        ),
    ]