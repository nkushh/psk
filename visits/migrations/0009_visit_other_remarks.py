# Generated by Django 2.0.2 on 2018-05-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0008_remove_visit_other_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='other_remarks',
            field=models.TextField(default=''),
        ),
    ]
