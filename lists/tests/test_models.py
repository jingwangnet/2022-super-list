from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import List, Item
from django.contrib.auth import get_user_model


User = get_user_model()


class ItemModelTest(TestCase):

    def test_value_of_default_item(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)
        self.assertEqual(item.text, '')

    def test_items_relate_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)

        self.assertIn(item, list_.item_set.all())


    def test_cannot_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_duplicate_item(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='bla')
        item = Item(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_can_save_duplicate_item_on_diffent_list(self):
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text='bla')
        correct_list = List.objects.create()
        item = Item.objects.create(list=correct_list, text='bla')

        item.full_clean() ## Should not raise errors

    def test_odering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text='1', list=list_)
        item2 = Item.objects.create(text='two', list=list_)
        item3 = Item.objects.create(text='3', list=list_)

        self.assertEqual(
            list(list_.item_set.all()),
            [item1, item2, item3]
        )

    def test_str(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='A item', list=list_)
        self.assertEqual(str(item), 'A item')
        

class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(
            list_.get_absolute_url(),
            f'/lists/{list_.pk}/'
        )

    def test_lists_can_have_owners(self):
        user = User.objects.create(email='a@b.com')
        list_ = List.objects.create(owner=user)
        self.assertIn(list_, user.list_set.all())

    def test_lists_owner_is_optional(self):
        List.objects.create() # Should not raise errors

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')






