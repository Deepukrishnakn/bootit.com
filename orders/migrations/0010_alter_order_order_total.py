# Generated by Django 4.0.4 on 2022-06-17 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_total',
            field=models.FloatField(null=True),
        ),
    ]
