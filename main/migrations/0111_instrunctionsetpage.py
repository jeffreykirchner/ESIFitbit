# Generated by Django 3.1.4 on 2021-03-15 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0110_auto_20210315_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrunctionSetPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_block', models.CharField(choices=[('ONE', 'ONE'), ('TWO', 'TWO'), ('THREE', 'THREE')], max_length=100)),
                ('page_type', models.CharField(choices=[('HEART', 'HEART'), ('SLEEP', 'SLEEP'), ('PAY', 'PAY')], max_length=100)),
                ('text', models.CharField(default='', max_length=50000, verbose_name='Text')),
                ('instruction_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.instrunctionset')),
            ],
            options={
                'verbose_name': 'Session Instuction Set Page',
                'verbose_name_plural': 'Session Instuction Set Pages',
                'ordering': ['instruction_set', 'time_block', 'page_type'],
            },
        ),
    ]
