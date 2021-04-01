# Pop-Corner

## Setup
Make sure you are in a virtual environment with python installed in order to proceed. 
### Install Dependencies:
All dependencies have been placed in the requirements.txt so running the following command should install all possible dependecies. 
```sh
(env)$ pip install -r requirements.txt
```
### Make Migrations:
Make sure to update to the latest migration with the following commands. 
```sh
(env)$ python manage.py makemigrations
```
```sh
(env)$ python manage.py migrate
```

## Run Application
Run the web application with the following command. 
```sh
(env)$ python manage.py runserver
```
### Clear Dataform
Since we are in the initial phases of web development, we do not necessarily want to always have this data in our databases when we're running tests. So the following commands are used to clear the data in the MyUser database from movies.models.py and also from the built in django User model.
```sh
>>> python manage.py shell
```
```sh
>>> from movies.models import MyUser
```
```sh
>>> MyUser.objects.all().delete()
```
```sh
>>> from django.contrib.auth.models import User
```
```sh
>>> User.objects.all().delete()
```

## Tests
The following command will run the tests specified in tests.py. 
```sh
(env)$ python manage.py tests
```

