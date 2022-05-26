from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from django.utils.html import escape
from django.contrib.auth import get_user_model
from lists.views import home_page
from lists.models import Item, List
from lists.forms import (
    ItemForm, EMPTY_ITEM_ERROR, 
    ExistingListItemForm, DUPLICATE_ITEM_ERROR
)
import unittest


User = get_user_model()

# Create your tests here.
class HomePageTest(TestCase):

    def test_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_use_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
        

   
class NewListTest(TestCase):

    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new item'})

        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')

    def test_redirect_after_post_request(self):
        response = self.client.post('/lists/new', data={'text': 'A new item'})
        html = response.content.decode()
        list_ = List.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{list_.pk}/')

    def test_validation_error_use_view_template(self):
        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_error_are_shown_in_template(self):
        response = self.client.post('/lists/new', data={'text': ''})

        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_validation_error_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invliad_list_items_arent_saved(self):
        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)

    def test_list_owner_isaved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        response = self.client.post('/lists/new', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)



class ViewListTest(TestCase):

    def test_use_view_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.pk}/')
        self.assertTemplateUsed(response, 'view.html')

    def test_render_only_items_for_that_list_in_template(self):
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text="First other item")
        Item.objects.create(list=other_list, text="Second other item")
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="First item")
        Item.objects.create(list=list_, text="Second item")

        response = self.client.get(f'/lists/{list_.pk}/')
        self.assertContains(response, 'First item')
        self.assertContains(response, 'Second item')
        self.assertNotContains(response, 'First other item')
        self.assertNotContains(response, 'Second other item')

    def test_pass_correct_list_instance(self):
        other_list = List.objects.create()
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.pk}/')
        self.assertEqual(response.context['list'], list_)

    def test_view_list_use_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.pk}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_can_save_POST_request_to_an_existing_list(self):
        list_ = List.objects.create()
        self.client.post(f'/lists/{list_.pk}/', data={'text': 'A new item'})

        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new item')

    def test_redirect_after_post_request(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.pk}/', data={'text': 'A new item'})
        html = response.content.decode()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{list_.pk}/')

    def post_invalid_request(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.pk}/', data={'text': ''})

    def test_invalid_post_nothting_to_db(self):
        response = self.post_invalid_request()

        self.assertEqual(0, Item.objects.count())

    def test_validation_error_use_view_template(self):
        response = self.post_invalid_request()

        self.assertTemplateUsed(response, 'view.html')

    def test_validation_error_are_show_in_template(self):
        response = self.post_invalid_request()

        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_validation_error_passes_form_to_tempate(self):
        response = self.post_invalid_request()

        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_duplicate_errors_end_up_on_template(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla', list=list_)
        response = self.client.post(f'/lists/{list_.pk}/', data={'text': 'bla'})

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'view.html')
        self.assertContains(response, escape(DUPLICATE_ITEM_ERROR))
        self.assertEqual(1, Item.objects.count())

class MyListsTest(TestCase):
    
    def test_my_lists_url_render_my_lists_template(self):
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)
