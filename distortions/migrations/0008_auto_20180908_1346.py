# Generated by Django 2.0.5 on 2018-09-08 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distortions', '0007_auto_20180908_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traplog',
            name='log_time',
            field=models.DateTimeField(verbose_name='logged at'),
        ),
    ]