# Generated by Django 4.0.4 on 2022-06-12 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_rename_variation_category_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]