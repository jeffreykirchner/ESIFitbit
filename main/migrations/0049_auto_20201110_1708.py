# Generated by Django 3.1.2 on 2020-11-10 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_auto_20201110_0004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session_subject_questionnaire1',
            old_name='exercise_hours',
            new_name='exercise_minutes',
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire1',
            name='exercise_importance',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Very Unimportant'), ('2', 'Unimportant'), ('3', 'Somewhat Unimportant'), ('4', 'Neutral'), ('5', 'Somewhat Important'), ('6', 'Important'), ('7', 'Very Important')], max_length=100, verbose_name='Exercise Likert'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire1',
            name='exercise_variation',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Very High'), ('2', 'High'), ('3', 'Somewhat High'), ('4', 'Average'), ('5', 'Somewhat Low'), ('6', 'Low'), ('7', 'Very Low')], max_length=100, verbose_name='Exercise Variation Likert'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire1',
            name='health_importance',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Very Unimportant'), ('2', 'Unimportant'), ('3', 'Somewhat Unimportant'), ('4', 'Neutral'), ('5', 'Somewhat Important'), ('6', 'Important'), ('7', 'Very Important')], max_length=100, verbose_name='Health Importance Likert'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire1',
            name='health_satisfaction',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Very Unsatisfied'), ('2', 'Unsatisfied'), ('3', 'Somewhat Unsatisfied'), ('4', 'Neutral'), ('5', 'Somewhat Satisfied'), ('6', 'Satisfied'), ('7', 'Very Satisfied')], max_length=100, verbose_name='Health Satisfaction Likert'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire1',
            name='sleep_importance',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Very Unimportant'), ('2', 'Unimportant'), ('3', 'Somewhat Unimportant'), ('4', 'Neutral'), ('5', 'Somewhat Important'), ('6', 'Important'), ('7', 'Very Important')], max_length=100, verbose_name='Sleep Likert'),
        ),
        migrations.AlterField(
            model_name='session_subject_questionnaire1',
            name='sleep_variation',
            field=models.CharField(choices=[('0', 'N/A'), ('1', 'Very High'), ('2', 'High'), ('3', 'Somewhat High'), ('4', 'Average'), ('5', 'Somewhat Low'), ('6', 'Low'), ('7', 'Very Low')], max_length=100, verbose_name='Sleep Variation Likert'),
        ),
    ]
