from django.test import TestCase
from lists.views import home_page
from lists.models import Item
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

        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')

        self.assertIn('A new item', html)
        self.assertTemplateUsed(response, 'home.html')

    def test_save_item_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(0, Item.objects.count())
   
    
class ItemModelTest(TestCase):

   def test_create_items_and_retrieve_it_later(self):
       first_item = Item()
       first_item.text = 'First item'
       first_item.save()

       second_item = Item()
       second_item.text = 'Second item'
       second_item.save()

       self.assertEqual(2, Item.objects.count())
       saved_first_item, saved_second_item = Item.objects.all()

       self.assertEqual(saved_first_item.text, 'First item')
       self.assertEqual(saved_second_item.text, 'Second item')
       
