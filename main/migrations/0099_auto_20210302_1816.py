# Generated by Django 3.1.4 on 2021-03-02 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0098_auto_20210302_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session_subject_questionnaire2',
            name='gender_identity',
            field=models.CharField(choices=[('', ''), ('Man', 'Man'), ('Woman', 'Woman'), ('FillIn', 'Write in below')], max_length=100, verbose_name='To which gender identity do you most identify?'),
        ),
    ]