# Generated by Django 3.1.7 on 2021-03-10 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='AvailableTickets',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='TotalTickets',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='movie',
            name='MovieDuration',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='TicketsReserved',
            field=models.IntegerField(),
        ),
    ]