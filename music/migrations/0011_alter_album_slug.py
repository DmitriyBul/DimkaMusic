# Generated by Django 4.0.3 on 2022-06-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_playlist_userplaylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
