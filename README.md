# Pop-Corner

## Setup
Make sure you are in a virtual environment with python installed in order to proceed. 
### Install Dependencies:
All dependencies have been placed in the requirements.txt so running the following command should install all possible dependecies. 
```sh
(venv)$ pip install -r requirements.txt
```
### Make Migrations:
Make sure to update to the latest migration with the following commands. 
```sh
(venv)$ python manage.py makemigrations
```
```sh
(venv)$ python manage.py migrate
```

## Run Application
Run the web application with the following command. 
```sh
(venv)$ python manage.py runserver
```

## Testing
The following command will run the tests specified in tests.py. 
```sh
(venv)$ python manage.py test
```

