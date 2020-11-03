# Generated by Django 3.1.2 on 2020-11-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_auto_20201103_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameterset',
            name='block_1_heart_pay',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='parameterset',
            name='block_1_immune_pay',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]