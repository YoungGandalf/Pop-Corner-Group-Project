# Generated by Django 3.2 on 2021-04-16 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExistingLocations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('lat', models.DecimalField(decimal_places=15, max_digits=18)),
                ('lng', models.DecimalField(decimal_places=15, max_digits=18)),
            ],
        ),
    ]
