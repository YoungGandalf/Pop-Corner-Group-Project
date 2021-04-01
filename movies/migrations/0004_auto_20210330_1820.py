# Generated by Django 3.1.7 on 2021-03-30 18:20

from django.db import migrations, models
import movies.validators


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20210327_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='UserName',
            field=models.CharField(max_length=100, validators=[movies.validators.validate_name_length, movies.validators.validate_username_alphadigits]),
        ),
        migrations.AlterField(
            model_name='user',
            name='UserPassword',
            field=models.CharField(max_length=256, validators=[movies.validators.validate_password_length, movies.validators.validate_password_digit, movies.validators.validate_password_uppercase]),
        ),
        migrations.AlterField(
            model_name='user',
            name='UserPhoneNumber',
            field=models.CharField(max_length=20, validators=[movies.validators.validate_phonenumber]),
        ),
    ]