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
### Using PopCorner:
Would recommend using the website with the following steps:
  1. /signup: Create a Business Owner Account (click the IsBusiness checkbox in the signup page)
  2. /movies: View all the possible movies in the slideshow (click on the event redirect at the bottom)
  3. /event: Create a new event
  4. Click on the logout button to logout
  5. /signup: Create a Normal User Account (use a valid email address you can access to test password recovery/notifications)
  6. /map: Click the locations tab to view the map and the markers (choose any of the markers to get redirected to the reservation page)
  7. /reservation: Create a reservation 
  8. /payment or /add: If you don't have any payment information in the database, you will be prompted to enter in new payment information. If you already had payment information on file, you will be redirected to the add page where you can choose one of the cards to pay. 
  9. Check your email. You should have an email about the reservation and the purchase. 
  10. /edit_reservation: Choose the Account Tab and you can view all your reservations, Click on a reservation and hit submit to remove the reservation entirely
  11. Click on the logout button to logout
  12. /login: Click on forgot password
  13. /password-reset: Enter the email associated with the Normal User Account
  14. Check your email. You should have an email with a link to reset the password. Go to the link and you will be prompted to change your password. 

## Testing
The following command will run the tests specified in tests.py. 
```sh
(venv)$ python manage.py test
```

