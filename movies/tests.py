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

    # Testing User View with Valid Data (Should head to the appropriate payment page, check!!!!)
    def test_add_valid_reservation_view(self):
        # Valid Data
        response = self.client.post(reverse('reservation'),
                                    data={'tickets': '2', 'tempID': '1'})
        self.assertEqual(response.status_code, 200)

    # Testing User View with Invalid Data (Should refresh back to the same page)
    def test_add_invalid_reservation_view(self):
        # Invalid data fails.
        response = self.client.post(reverse('reservation'),
                                    data={'tickets': '-15', 'tempID': '1'}, follow=True)
        self.assertEqual(response.status_code, 200)


# Tests for Event Form
class EventTestCases(TestCase):
    def test_EventTestCases_valid(self):
        MyUser.objects.create(UserEmail="ownertest1@gmail.com", UserPassword="Owner1", UserName="ownertest1",
                              UserPhoneNumber="123-456-7899", IsBusiness=True)
        Movie.objects.create(MovieName="TestMovie", MovieDuration="60")
        form = EventForm(data={'EventAddress': "123", 'AvailableTickets': '90',
                               'TotalTickets': '100', 'EventDate': "2021-10-25",
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
        # response = self.client.get(reverse('/password-reset-confirm/' + str(base64.b64encode(bytes(user.id))) +
        #                                  '/' + str(token)), {'new_password1:Lemons123', 'new_password2:Lemons123'})
        # self.assertEqual(response.status_code, 302)

        # once the password is change, checks if the login is correct
        # BECAUSE THE ABOVE STATEMENT DOES NOT WORK, THIS STATEMENT IS FALSE
        # self.assertTrue(self.client.login(username='testing', password='Lemons123'))


# Tests for creating a reservation
class EditReservationTestCase(TestCase):
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
                          AvailableTickets=8, TotalTickets=10, EventDate='2021-10-25 10:20:01', MovieId_id=1,
                          EventWebsite="www.business.com")
        testEvent.save()
        testReservation = Reservation(Owner_id="owner@gmail.com", EventId_id=1, TicketsReserved=2)
        testReservation.save()
        user = User.objects.create_user(username='testing', password='Testing123')
        self.client.login(username='testing', password='Testing123')

    # Testing no checkbox which will redirect back to the same page and the reservation will still exist
    def test_delete_reservation(self):
        response = self.client.post(reverse('delete_reservation'),
                                    data={'res': ''})
        self.assertTrue(Reservation.objects.filter(ReservationId=1))
        self.assertEqual(response.status_code, 200)

    # Testing a checkbox was selected will redirect back to the same page and delete the reservation
    def test_delete_reservation(self):
        response = self.client.post(reverse('delete_reservation'),
                                    data={'res': '1'})
        # Check the reservation does not exist in the database anymore
        self.assertFalse(Reservation.objects.filter(ReservationId=1))
        self.assertEqual(response.status_code, 200)


class PaymentRedirectTestCase(TestCase):

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

    # Test that user is redirected to the add payment page when no card is stored on the account
    def test_add_payment_redirect(self):
        response = self.client.post(reverse('add'), {'tickets': '2', 'tempID': '1'}, follow=True)
        self.assertRedirects(response, reverse('payment'), status_code=302)

    # Test that user is taken to payment selection page if card is registered with account
    def test_select_payment_redirect(self):
        testCard = Payment(Owner_id="testing@gmail.com", CardNumber="1234567890123456", ExpDate="02/23", SecCode="123",
                           Address="no", ZipCode="21146")
        testCard.save()

        response = self.client.post(reverse('add'), {'tickets': '2', 'tempID': '1'}, follow=True)
        self.assertEqual(response.status_code, 200)


# Test to make sure that emails are sent properly
class EmailTestCase(TestCase):

    # Loads all the information into the database
    def setUp(self):
        testUser = MyUser(UserEmail="testing@gmail.com", UserPassword="Testing123", UserName="testing",
                          UserPhoneNumber="123-456-7890", IsBusiness=False)
        testUser.save()
        testMovie = Movie(MovieName="Aladdin", MovieDuration="128")
        testMovie.save()
        testEvent = Event(Owner_id="testing@gmail.com", EventAddress="5142 Owner Road Business California 12345",
                          AvailableTickets=10, TotalTickets=10, EventDate='2021-10-25 10:20:01', MovieId_id=1,
                          EventWebsite="www.business.com")
        testEvent.save()

    # Checks the simple case once an email is sent: verifies the subject, content, and sender
    def test_successful_simple_sent_email(self):
        testUser = MyUser.objects.get(UserEmail="testing@gmail.com")
        mail.send_mail('testing',
                       'message',
                       settings.EMAIL_HOST_USER,
                       [testUser.UserEmail]
                       )

        # Test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct
        self.assertEqual(mail.outbox[0].subject, 'testing')

        # Verify that the sender of the first message is correct
        self.assertEqual(mail.outbox[0].from_email, 'popcorner447@gmail.com')

        # Verifies the content of the first message
        self.assertEqual(mail.outbox[0].body, 'message')

    def test_successful_template_sent_email(self):
        testUser = MyUser.objects.get(UserEmail="testing@gmail.com")
        testEvent = Event.objects.get(EventWebsite="www.business.com")
        testMovie = Movie.objects.get(MovieName="Aladdin")

        template = render_to_string('movies/email_template.html', {'name': testUser.UserName,
                                                                   'num_tickets': 5,
                                                                   'event_name': testMovie.MovieName,
                                                                   'event_date': testEvent.EventDate,
                                                                   'event_location': testEvent.EventAddress})
        mail.send_mail(testUser.UserName,
                       template,
                       settings.EMAIL_HOST_USER,
                       [testUser.UserEmail]
                       )

        # Test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct
        self.assertEqual(mail.outbox[0].subject, 'testing')

        # Verify that the sender of the first message is correct
        self.assertEqual(mail.outbox[0].from_email, 'popcorner447@gmail.com')

        # Checks that the template was used and the correct movie name is inside
        self.assertIn('Aladdin', mail.outbox[0].body, 'key is not in container')
