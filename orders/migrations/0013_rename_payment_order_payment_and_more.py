# Generated by Django 4.0.4 on 2022-06-17 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_remove_orderproduct_color_remove_orderproduct_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Payment',
            new_name='payment',
        ),
        migrations.RenameField(
            model_name='orderproduct',
            old_name='Order',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderproduct',
            old_name='Payment',
            new_name='payment',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='Payment_id',
            new_name='payment_id',
        ),
    ]
