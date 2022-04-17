from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from django.urls import resolve

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_use_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
   
    
