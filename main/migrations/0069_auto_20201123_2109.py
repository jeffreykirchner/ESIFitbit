# Generated by Django 3.1.2 on 2020-11-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0068_parameters_paymenthelptextbaseline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='treatment',
            field=models.CharField(choices=[('B', 'Baseline'), ('I', 'Individual'), ('IwC', 'Individual with chat'), ('IwCpB', 'Individual with chat and bonus')], default='I', max_length=100),
        ),
    ]