# Generated by Django 3.2 on 2021-05-06 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_remove_watchlist_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='Favorites',
            field=models.BooleanField(default=False),
        ),
    ]
