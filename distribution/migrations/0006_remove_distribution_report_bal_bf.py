# Generated by Django 2.0.2 on 2018-10-09 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0005_auto_20180502_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distribution_report',
            name='bal_bf',
        ),
    ]
