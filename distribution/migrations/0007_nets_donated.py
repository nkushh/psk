# Generated by Django 2.0.2 on 2018-10-22 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0006_remove_distribution_report_bal_bf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nets_donated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beneficiary', models.CharField(max_length=200)),
                ('invoice_no', models.CharField(default='', max_length=200)),
                ('warehouse', models.CharField(default='', max_length=255)),
                ('nets_issued', models.IntegerField()),
                ('donor_code', models.CharField(default='', max_length=20)),
                ('date_issued', models.DateField()),
                ('date_recorded', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]
