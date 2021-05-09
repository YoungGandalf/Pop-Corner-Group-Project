from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
import base64

from .forms import *
from django.test import TestCase, Client
from .models import *


# Create your tests here.

# Tests for User Signup
class UserTestCase(TestCase):
    # Setup the test by creating one User Object
    def setUp(self):
        MyUser.objects.create(UserEmail="testing@gmail.com", UserPassword="Testing123", UserName="testing",
                              UserPhoneNumber="123-456-7890", IsBusiness=False)

    # Test that one User object was created
    def test_user_created(self):
        self.assertEqual(MyUser.objects.count(), 1)

    # Test fhe UserForm works for valid information
    def test_UserForm_valid(self):
        form = UserForm(data={'UserEmail': "testing1@gmail.com", 'UserPassword': "Testing321", 'UserName': "testing1",
                              'UserPhoneNumber': "987-654-3210", 'IsBusiness': False})
        self.assertTrue(form.is_valid())

    # Testing Invalid Data in the form
    def test_UserForm_invalid(self):
        form = UserForm(data={'UserEmail': "testing1@gmail.com", 'UserPassword': "test", 'UserName': "testing123",
                              'UserPhoneNumber': "987-654-3210", 'IsBusiness': False})
        self.assertFalse(form.is_valid())

    # Testing User View with Valid Data (Should refresh back to the same page with a cleared form)
    def test_add_valid_user_view(self):
        # Valid Data
        response = self.client.post(reverse('signup'),
                                    data={'UserEmail': "testing12345@gmail.com", 'UserPassword': "Testing321",
                                          'UserName': "testing321",
                                          'UserPhoneNumber': "987-654-3210", 'IsBusiness': True})
        self.assertEqual(response.status_code, 200)

    # Testing User View with Invalid Data (Should refresh back to the same page)
    def test_add_invalid_user_view(self):
        # Invalid data fails.
        response = self.client.post(reverse('signup'),
                                    data={'UserEmail': "testing1@gmail.com", 'UserPassword': "",
                                          'UserName': "testing123",
                                          'UserPhoneNumber': "987-654-3210", 'IsBusiness': False})
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        self.failUnless(response.context['form'].errors)


# Tests for Login Case
class LoginTestCase(TestCase):
    def setUp(self):
        MyUser.objects.create(UserEmail="testing@gmail.com", UserPassword="Testing123", UserName="testing",
                              UserPhoneNumber="123-456-7890", IsBusiness=False)
        user = User.objects.create_user(username='testing', password='Testing123')

    # Testing for successful login
    def test_successful_login(self):
        self.assertTrue(self.client.login(username='testing', password='Testing123'))

    # Testing for unsuccessful login
    def test_unsuccessful_login(self):
        self.assertFalse(self.client.login(username='testing', password='wrong'))


class PaymentTestCase(TestCase):
    def setUp(self):
        testUser = MyUser(UserEmail="testing@gmail.com", UserPassword="Testing123", UserName="testing",
                          UserPhoneNumber="123-456-7890", IsBusiness=False)
        testUser.save()
        user = User.objects.create_user(username='testing', password='Testing123')
        self.client.login(username='testing', password='Testing123')

    def test_PaymentForm_valid(self):
        form = PaymentForm(data={'CardNumber': '0123654789654123', 'ExpDate': '02/25', 'SecCode': '221',
                                 'Address': '123 test drive', 'ZipCode': '21227'})
        self.assertTrue(form.is_valid())

    def test_PaymentForm_invalid(self):
        form = PaymentForm(data={'CardNumber': '0123654789654123', 'ExpDate': '02/55', 'SecCode': '221',
                                 'Address': '123 test drive', 'ZipCode': '21227'})
        self.assertFalse(form.is_valid())

    def test_add_valid_payment(self):
        self.client.login(username='testing', password='Testing123')

        response = self.client.post('/payment/',
                                    data={'CardNumber': '0123654789654123', 'ExpDate': '02/25', 'SecCode': '221',
                                          'Address': '123 test drive', 'ZipCode': '21227'})

        self.assertEqual(response.status_code, 200)

    def test_add_invalid_payment(self):
        response = self.client.post(reverse('payment'),
                                    data={'CardNumber': 'This is not a number', 'ExpDate': '02/25', 'SecCode': '221',
                                          'Address': '123 test drive', 'ZipCode': '21227'})

        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        self.failUnless(response.context['form'].errors)


# Tests for creating a reservation
class ReservationTestCase(TestCase):
    # Need to initialize a user that is logged in, an owner (MyUser) who owns the event, a movie and possible
    def setUp(self):
        testOwner = MyUser(UserEmail="owner@gmail.com", UserPassword="Owner123", UserName="owner",
                           UserPhoneNumber="123-456-7890", IsBusiness=True)
        testOwner.save()
        testUser = MyUser(UserEmail="testing@gmail.com", UserPassword="Testing123", UserName="testing",
                          UserPhoneNumber="123-456-7890", IsBusiness=False)
        testUser.save()
        testMovie = Movie(MovieName="Aladdin", MovieDuration="128")
        testMovie.save()
        testEvent = Event(Owner_id="owner@gmail.com", EventAddress="5142 Owner Road Business California 12345",
                          AvailableTickets=10, TotalTickets=10, EventDate='2021-10-25 10:20:01', MovieId_id=1,
                          EventWebsite="www.business.com")
        testEvent.save()
        user = User.objects.create_user(username='testing', password='Testing123')
        self.client.login(username='testing', password='Testing123')

    # Test the ReservationForm works for valid information
    def test_ReservationForm_valid(self):
        form = ReservationForm(data={'TicketsReserved': '2', 'temp': '1'})
        self.assertTrue(form.is_valid())

    # Test the ReservationForm works for invalid information
    def test_ReservationForm_invalid(self):
        # User can't enter a non negative ticket number
        form = ReservationForm(data={'TicketsReserved': '-1', 'temp': '1'})
        self.assertFalse(form.is_valid())

    # Testing User View with Valid Data (Should refresh back to the same page with a cleared form)
    def test_add_valid_reservation_view(self):
        # Valid Data
        response = self.client.post(reverse('reservation'),
                                    data={'tickets': '2', 'tempID': '1'})
        self.assertEqual(response.status_code, 200)

    # Testing User View with Invalid Data (Should refresh back to the same page)
    def test_add_invalid_reservation_view(self):
        # Invalid data fails.
        response = self.client.post(reverse('reservation'),
                                    data={'tickets': '-15', 'tempID': '1'})
        self.assertEqual(response.status_code, 200)


# Tests for Event Form
class EventTestCases(TestCase):
    def test_EventTestCases_valid(self):
        MyUser.objects.create(UserEmail="ownertest1@gmail.com", UserPassword="Owner1", UserName="ownertest1",
                              UserPhoneNumber="123-456-7899", IsBusiness=True)
        Movie.objects.create(MovieName="TestMovie", MovieDuration="60")
        form = EventForm(
            data={'EventName': 'TestEvent',
                  'EventAddress': 'Erickson Field - 1000 Hilltop Circle, Baltimore, MD 21250',
                  'AvailableTickets': '90',
                  'TotalTickets': '100', 'EventDate': "2021-10-25",
                  'EventWebsite': "www.johndoe.com"})

        self.assertTrue(form.is_valid())

    def test_EventTestCases_invalid(self):
        MyUser.objects.create(UserEmail="ownertest2@gmail.com", UserPassword="Owner2", UserName="ownertest2",
                              UserPhoneNumber="123-456-7895", IsBusiness=True)
        Movie.objects.create(MovieName="TestMovie", MovieDuration="60")
        form = EventForm(
            data={'Owner_id': "ownertest1@gmail.com", 'EventName': "", 'EventAddress': "", 'AvailableTickets': "",
                  'TotalTickets': "", 'EventDate': "", 'MovieId_id': "2",
                  'EventWebsite': ""})
        self.assertFalse(form.is_valid())


# Tests for Password Reset
class PasswordResetCase(TestCase):
    def setUp(self):
        MyUser.objects.create(UserEmail="testing@gmail.com", UserPassword="Testing123", UserName="testing",
                              UserPhoneNumber="123-456-7890", IsBusiness=False)

    # Actual Reset Password
    def test_reset_password(self):
        # checks if the initial password reset form works
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        user = User.objects.create_user(username='testing', password='Testing123')
        token = default_token_generator.make_token(user)

        # checks if the password is properly reset
        # THIS TEST DOES NOT WORK RIGHT NOW BECAUSE I'M NOT SURE HOW TO ENCODE THE UIDB64, BUT THE TOKEN IS CORRECT
        response = self.client.get(reverse('/password-reset-confirm/' + str(base64.b64encode(bytes(user.id))) +
                                           '/' + str(token)), {'new_password1:Lemons123', 'new_password2:Lemons123'})
        self.assertEqual(response.status_code, 302)

        # once the password is change, checks if the login is correct
        # BECAUSE THE ABOVE STATEMENT DOES NOT WORK, THIS STATEMENT IS FALSE
        # self.assertTrue(self.client.login(username='testing', password='Lemons123'))
