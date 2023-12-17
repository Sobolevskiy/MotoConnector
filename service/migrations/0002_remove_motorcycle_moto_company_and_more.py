# Generated by Django 4.2.7 on 2023-12-06 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motorcycle',
            name='moto_company',
        ),
        migrations.RemoveField(
            model_name='motorcycle',
            name='moto_model',
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='cc',
            field=models.IntegerField(choices=[(0, '0-200'), (10, '200-500'), (20, '500-700'), (30, '700-1000'), (40, '>1000')], default=0),
        ),
        migrations.DeleteModel(
            name='MotoCompany',
        ),
        migrations.DeleteModel(
            name='MotoModel',
        ),
    ]
