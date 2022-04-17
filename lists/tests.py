from django.test import TestCase
from lists.views import home_page
from lists.models import Item, List
from django.http import HttpRequest
from django.urls import resolve

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_use_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_save_item_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(0, Item.objects.count())
   
class NewListTest(TestCase):

    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'new_item': 'A new item'})

        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')

    def test_redirect_after_post_request(self):
        response = self.client.post('/lists/new', data={'new_item': 'A new item'})
        html = response.content.decode()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-url/')

class ViewListTest(TestCase):

    def test_home_page_use_template(self):
        response = self.client.get('/lists/the-only-url/')
        self.assertTemplateUsed(response, 'view.html')

    def test_render_all_items_in_template(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="First item")
        Item.objects.create(list=list_, text="Second item")

        response = self.client.get('/lists/the-only-url/')
        self.assertContains(response, 'First item')
        self.assertContains(response, 'Second item')
    
class ListAndItemModelTest(TestCase):

   def test_create_items_and_retrieve_it_later(self):
       list_ = List()
       list_.save()
       first_item = Item()
       first_item.text = 'First item'
       first_item.list = list_
       first_item.save()

       second_item = Item()
       second_item.text = 'Second item'
       second_item.list = list_
       second_item.save()

       self.assertEqual(2, Item.objects.count())
       self.assertEqual(1, List.objects.count())
       saved_list = List.objects.first()
       saved_first_item, saved_second_item = saved_list.item_set.all() 

       self.assertEqual(saved_first_item.text, 'First item')
       self.assertEqual(saved_first_item.list, list_)
       self.assertEqual(saved_second_item.text, 'Second item')
       self.assertEqual(saved_second_item.list, list_)
       
