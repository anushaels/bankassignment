# Generated by Django 5.1.1 on 2024-09-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0003_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]