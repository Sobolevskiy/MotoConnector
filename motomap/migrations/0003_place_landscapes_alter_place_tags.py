# Generated by Django 4.2.7 on 2024-02-04 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motomap', '0002_landscape_placetag_place_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='landscapes',
            field=models.ManyToManyField(blank=True, related_name='landscapes', to='motomap.landscape'),
        ),
        migrations.AlterField(
            model_name='place',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='motomap.placetag'),
        ),
    ]
