# Generated by Django 2.0.2 on 2018-09-03 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0008_facilities_added_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilities',
            name='added_by',
        ),
    ]
