from django.contrib.auth.models import User
from django.urls import reverse

from movies.forms import *
from django.test import TestCase, Client
from movies.models import *


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
