# Generated by Django 4.0.4 on 2022-06-06 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_subcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Subcategory',
            new_name='SubCategory',
        ),
    ]