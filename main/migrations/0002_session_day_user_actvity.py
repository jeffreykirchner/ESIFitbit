# Generated by Django 3.1.2 on 2020-10-16 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session_day_user_actvity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heart_activity_minutes', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('immune_activity_minutes', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('heart_activity', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('immune_activity', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('check_in_today', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('session_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.session_day')),
                ('session_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.session_subject')),
            ],
            options={
                'verbose_name': 'Session Day',
                'verbose_name_plural': 'Session Dat',
            },
        ),
    ]
