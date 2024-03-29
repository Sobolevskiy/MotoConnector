# Generated by Django 4.2.7 on 2024-03-18 13:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('motomap', '0006_place_discoverer'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='placeimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='placeimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
