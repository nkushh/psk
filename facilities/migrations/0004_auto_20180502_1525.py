# Generated by Django 2.0.2 on 2018-05-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_facilities_constituency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilities',
            name='epidemiological_zone',
            field=models.CharField(default='', max_length=200),
        ),
    ]
