from django.urls import reverse

from movies.forms import forms, UserForm
from django.test import TestCase
from movies.models import User


# Create your tests here.

# Tests for User Signup
class UserTestCase(TestCase):
    # Setup the test by creating one User Object
    def setUp(self):
        User.objects.create(UserEmail="testing@gmail.com", UserPassword="Testing123", UserName="testing",
                            UserPhoneNumber="123-456-7890", IsBusiness=False)

    # Test that one User object was created
    def test_user_created(self):
        self.assertEqual(User.objects.count(), 1)

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

    # Testing User View with Invalid Data (Should refresh back to the same page)
    def test_add_user_view(self):
        # Invalid data fails.
        response = self.client.post(reverse('signup'),
                                    data={'UserEmail': "testing1@gmail.com", 'UserPassword': "",
                                          'UserName': "testing123",
                                          'UserPhoneNumber': "987-654-3210", 'IsBusiness': False})
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        self.failUnless(response.context['form'].errors)
