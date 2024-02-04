# Generated by Django 4.2.7 on 2024-02-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motomap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Landscape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='tags', to='motomap.placetag'),
        ),
    ]
