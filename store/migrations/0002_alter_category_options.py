# Generated by Django 4.0.4 on 2022-06-04 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'categrory', 'verbose_name_plural': 'categories'},
        ),
    ]
