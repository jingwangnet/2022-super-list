from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import List, Item


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


    def test_cannot_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()


