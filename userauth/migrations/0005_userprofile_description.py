# Generated by Django 4.2.7 on 2024-03-09 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0004_userprofile_instagram_userprofile_tg_userprofile_vk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
