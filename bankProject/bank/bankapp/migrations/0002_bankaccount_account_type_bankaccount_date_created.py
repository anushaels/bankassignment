# Generated by Django 5.1.1 on 2024-09-05 10:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='account_type',
            field=models.CharField(choices=[('savings', 'Savings'), ('current', 'Current')], default='savings', max_length=10),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
