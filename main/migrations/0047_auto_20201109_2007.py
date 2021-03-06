# Generated by Django 3.1.2 on 2020-11-09 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_auto_20201107_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='questionnaire1Required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='parameters',
            name='questionnaire2Required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='session_subject',
            name='questionnaire1_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='session_subject',
            name='questionnaire2_required',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Session_subject_questionnaire1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sleep_hours', models.DecimalField(decimal_places=1, default=0, max_digits=4, verbose_name='Sleep Hours')),
                ('sleep_importance', models.CharField(choices=[('1', 'Very Unimportant'), ('2', 'Unimportant'), ('3', 'Somewhat Unimportant'), ('4', 'Neutral'), ('5', 'Somewhat Important'), ('6', 'Important'), ('7', 'Very Important')], max_length=100, verbose_name='Sleep Likert')),
                ('sleep_explanation', models.CharField(default='', max_length=10000, verbose_name='Sleep Explanation')),
                ('session_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Session_subject_questionnaire1', to='main.session_subject')),
            ],
            options={
                'verbose_name': 'Pre Questionnaire',
                'verbose_name_plural': 'Pre Questionnaires',
            },
        ),
    ]
