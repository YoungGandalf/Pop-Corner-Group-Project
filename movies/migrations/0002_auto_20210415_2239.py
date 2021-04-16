# Generated by Django 3.2 on 2021-04-15 22:39

from django.db import migrations, models
import movies.validators


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='EventWebsite',
            field=models.URLField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='TicketsReserved',
            field=models.IntegerField(validators=[movies.validators.validate_tickets_reserved]),
        ),
    ]