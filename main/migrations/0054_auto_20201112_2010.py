# Generated by Django 3.1.2 on 2020-11-12 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_session_subject_questionnaire2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session_subject_questionnaire2',
            name='exercise_changed',
            field=models.CharField(choices=[('', ''), ('0', 'N/A'), ('1', 'Very much more'), ('2', 'Much more'), ('3', 'A little more'), ('4', 'The same'), ('5', 'A little less'), ('6', 'Much less'), ('7', 'Very much less')], max_length=100, verbose_name='Exercise Change Post'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire2',
            name='exercise_changed_explaination',
            field=models.CharField(default='', max_length=10000, verbose_name='Exercise Changed Post Explanation'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire2',
            name='health_concern',
            field=models.CharField(choices=[('', ''), ('0', 'N/A'), ('1', 'Very much more'), ('2', 'Much more'), ('3', 'A little more'), ('4', 'The same'), ('5', 'A little less'), ('6', 'Much less'), ('7', 'Very much less')], max_length=100, verbose_name='Health Concsern Post'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire2',
            name='health_concern_explaination',
            field=models.CharField(default='', max_length=10000, verbose_name='Health Concern Post Explanation'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire2',
            name='sleep_changed',
            field=models.CharField(choices=[('', ''), ('0', 'N/A'), ('1', 'Very much more'), ('2', 'Much more'), ('3', 'A little more'), ('4', 'The same'), ('5', 'A little less'), ('6', 'Much less'), ('7', 'Very much less')], max_length=100, verbose_name='Sleep Change Post'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire2',
            name='sleep_changed_explaination',
            field=models.CharField(default='', max_length=10000, verbose_name='Sleep Change Post Explanation'),
        ),
    ]
