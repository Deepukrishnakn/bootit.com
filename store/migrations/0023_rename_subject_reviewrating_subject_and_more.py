# Generated by Django 4.0.4 on 2022-06-28 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_reviewrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewrating',
            old_name='Subject',
            new_name='subject',
        ),
        migrations.RemoveField(
            model_name='reviewrating',
            name='image',
        ),
    ]