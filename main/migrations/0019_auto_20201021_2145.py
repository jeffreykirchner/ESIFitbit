# Generated by Django 3.1.2 on 2020-10-21 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20201021_1736'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parameterset',
            old_name='treatment_1_day_count',
            new_name='block_1_day_count',
        ),
        migrations.RenameField(
            model_name='parameterset',
            old_name='treatment_pay_1',
            new_name='block_1_heart_pay',
        ),
        migrations.RenameField(
            model_name='parameterset',
            old_name='treatment_2_day_count',
            new_name='block_2_day_count',
        ),
        migrations.RenameField(
            model_name='parameterset',
            old_name='treatment_pay_2',
            new_name='block_2_heart_pay',
        ),
        migrations.RenameField(
            model_name='parameterset',
            old_name='treatment_3_day_count',
            new_name='block_3_day_count',
        ),
        migrations.RenameField(
            model_name='parameterset',
            old_name='treatment_pay_3',
            new_name='block_3_heart_pay',
        ),
        migrations.AddField(
            model_name='parameterset',
            name='block_1_immune_pay',
            field=models.DecimalField(decimal_places=2, default=4.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='parameterset',
            name='block_2_immune_pay',
            field=models.DecimalField(decimal_places=2, default=8.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='parameterset',
            name='block_3_immune_pay',
            field=models.DecimalField(decimal_places=2, default=16.0, max_digits=6),
        ),
    ]
