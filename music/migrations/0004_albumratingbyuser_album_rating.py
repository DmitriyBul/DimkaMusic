# Generated by Django 4.0.3 on 2022-04-05 15:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_alter_song_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumRatingByUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, size=None)),
                ('users', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, size=None)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='rating',
            field=models.FloatField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
