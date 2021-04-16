from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
import base64
from movies.forms import forms, UserForm
from django.test import TestCase, Client
from movies.models import MyUser
import re


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

        #once the password is change, checks if the login is correct
        # BECAUSE THE ABOVE STATEMENT DOES NOT WORK, THIS STATEMENT IS FALSE
        #self.assertTrue(self.client.login(username='testing', password='Lemons123'))
