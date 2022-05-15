from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can't have an empty item"
DUPLICATE_ITEM_ERROR = "You've alredy added this item"

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text' : forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {
                'required': EMPTY_ITEM_ERROR,
            }
        }

    def save(self, for_list, *args, **kwargs):
        self.instance.list = for_list
        return super().save()
        

class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError:
            self.add_error('text', DUPLICATE_ITEM_ERROR)
