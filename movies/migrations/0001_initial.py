# Generated by Django 3.2 on 2021-05-09 17:02

from django.db import migrations, models
import django.db.models.deletion
import movies.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('EventId', models.AutoField(primary_key=True, serialize=False)),
                ('LocationName', models.CharField(max_length=100)),
                ('EventAddress', models.CharField(max_length=100)),
                ('AvailableTickets', models.IntegerField()),
                ('TotalTickets', models.IntegerField()),
                ('EventDate', models.DateTimeField()),
                ('EventWebsite', models.URLField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('MovieId', models.AutoField(primary_key=True, serialize=False)),
                ('MovieName', models.CharField(max_length=100)),
                ('MovieDuration', models.PositiveIntegerField()),
                ('MoviePic', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('UserEmail', models.EmailField(max_length=100, primary_key=True, serialize=False, validators=[movies.validators.validate_name_length])),
                ('UserPassword', models.CharField(max_length=256, validators=[movies.validators.validate_password_length, movies.validators.validate_password_digit, movies.validators.validate_password_uppercase])),
                ('UserName', models.CharField(max_length=100, validators=[movies.validators.validate_name_length, movies.validators.validate_username_alphadigits])),
                ('UserPhoneNumber', models.CharField(max_length=20, validators=[movies.validators.validate_phonenumber])),
                ('IsBusiness', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('WatchlistId', models.AutoField(primary_key=True, serialize=False)),
                ('MovieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.myuser')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('ReservationId', models.AutoField(primary_key=True, serialize=False)),
                ('TicketsReserved', models.IntegerField(validators=[movies.validators.validate_tickets_reserved])),
                ('EventId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.event')),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.myuser')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('PaymentId', models.AutoField(primary_key=True, serialize=False)),
                ('CardNumber', models.CharField(max_length=256, validators=[movies.validators.validate_card_number])),
                ('ExpDate', models.CharField(max_length=256, validators=[movies.validators.validate_expiration_date])),
                ('SecCode', models.CharField(max_length=256, validators=[movies.validators.validate_security_code])),
                ('Address', models.CharField(max_length=100)),
                ('ZipCode', models.CharField(max_length=10, validators=[movies.validators.validate_zip_code])),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.myuser')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='MovieId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie'),
        ),
        migrations.AddField(
            model_name='event',
            name='Owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.myuser'),
        ),
    ]
