from django.test import TestCase
from django.test import Client

# Create your tests here.


class testCases(TestCase):
    def setUp(self):
        pass

    def test_basic_response(self):
        c = Client()
        response = c.post('')
        self.assertEqual(response.status_code, 200)
