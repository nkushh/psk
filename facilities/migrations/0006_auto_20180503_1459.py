# Generated by Django 2.0.2 on 2018-05-03 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_facilities_system_balance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facilities',
            old_name='system_balance',
            new_name='system_net_balance',
        ),
    ]
