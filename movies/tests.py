from django.contrib.auth.models import User
from django.urls import reverse

from .forms import forms, UserForm, EventForm
from django.test import TestCase, Client
from .models import MyUser, Event, Movie


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
        self.client = Client()

    # Testing for successful login
    def test_successful_login(self):
        self.assertTrue(self.client.login(username='testing', password='Testing123'))

    # Testing for unsuccessful login
    def test_unsuccessful_login(self):
        self.assertFalse(self.client.login(username='testing', password='wrong'))


# Tests for Event Form
class EventTestCases(TestCase):
    def test_EventTestCases_valid(self):
        MyUser.objects.create(UserEmail="ownertest1@gmail.com", UserPassword="Owner1", UserName="ownertest1",
                              UserPhoneNumber="123-456-7899", IsBusiness=True)
        Movie.objects.create(MovieName="TestMovie", MovieDuration="60")
        form = EventForm(data={'Owner_id': "ownertest1@gmail.com", 'EventAddress': "123", 'AvailableTickets': "90",
                               'TotalTickets': "100", 'EventDate': "2021-10-25", 'MovieId_id': "1",
                               'EventWebsite': "www.johndoe.com"})
        self.assertTrue(form.is_valid())

    def test_EventTestCases_invalid(self):
        MyUser.objects.create(UserEmail="ownertest2@gmail.com", UserPassword="Owner2", UserName="ownertest2",
                              UserPhoneNumber="123-456-7895", IsBusiness=True)
        Movie.objects.create(MovieName="TestMovie", MovieDuration="60")
        form = EventForm(data={'Owner_id': "ownertest1@gmail.com", 'EventAddress': "", 'AvailableTickets': "",
                               'TotalTickets': "", 'EventDate': "", 'MovieId_id': "2",
                               'EventWebsite': ""})
        self.assertFalse(form.is_valid())
