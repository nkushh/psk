# Generated by Django 2.0.2 on 2018-05-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20180502_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilities',
            name='system_balance',
            field=models.IntegerField(default=0),
        ),
    ]
