from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from django.urls import resolve

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_use_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_POST_request(self):
        response = self.client.post('/', data={'new_item': 'A new item'})
        html = response.content.decode()
        self.assertIn('A new item', html)
        self.assertTemplateUsed(response, 'home.html')
   
    
