# Generated by Django 4.0.3 on 2022-04-09 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_usersalbumrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersalbumrating',
            name='rating',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
