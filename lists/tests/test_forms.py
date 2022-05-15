from django.test import TestCase
from django import forms
from lists.forms import (
    ItemForm, EMPTY_ITEM_ERROR,
    ExistingListItemForm, DUPLICATE_ITEM_ERROR
)
from lists.models import Item, List


class ItemFormTest(TestCase):

    def test_itemform_has_placeholder_and_css_class(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_validation_form_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_save_handel_saving_to_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'A item'})
        form.save(for_list=list_)

        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A item')
        self.assertEqual(item.list, list_)

class ExistingListItemFormTest(TestCase):

    def test_ExistingListitemform_has_placeholder_and_css_class(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_validation_form_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(data={'text': ''}, for_list=list_)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_validation_form_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla', list=list_)
        form = ExistingListItemForm(data={'text': 'bla'}, for_list=list_)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [DUPLICATE_ITEM_ERROR]

        )

    def test_form_save_handel_saving_to_list(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(data={'text': 'A item'}, for_list=list_)
        form.save()

        self.assertEqual(1, Item.objects.count())
        item = Item.objects.first()
        self.assertEqual(item.text, 'A item')
        self.assertEqual(item.list, list_)
