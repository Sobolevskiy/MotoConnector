# Generated by Django 4.2.7 on 2024-03-09 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motomap', '0004_placeimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='location',
            new_name='geometry',
        ),
    ]
