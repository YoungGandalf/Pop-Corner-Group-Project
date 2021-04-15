from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse

from . import views

class MapPageTest(TestCase):
    def test_map_home_page(self):
        response = self.client.get('/map/')
        self.assertEquals(response.status_code, 200)

    def test_map_page_contains_map(self):
        response = self.client.get('/map/')
        self.assertContains(response, '<div id="map"></div>')

    def test_map_is_not_homepage(self):
        response = self.client.get('/map/')
        self.assertNotContains(response, 'Welcome to PopCorner!' )