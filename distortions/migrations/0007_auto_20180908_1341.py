# Generated by Django 2.0.5 on 2018-09-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distortions', '0006_auto_20180805_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='traplog',
            name='detail',
            field=models.TextField(null=True),
        ),
    ]