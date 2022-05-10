from django.test import TestCase
from django import forms
from lists.forms import ItemForm

class ItemFormTest(TestCase):

    def test_itemform_has_placeholder_and_css_class(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
