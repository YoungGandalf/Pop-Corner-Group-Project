# Generated by Django 3.2 on 2021-05-05 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_event_eventname'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='Favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='movies.MyUser'),
        ),
    ]
