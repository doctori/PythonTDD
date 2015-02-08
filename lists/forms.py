from django import forms
from django.core.exceptions import ValidationError
from lists.models import Item, List

EMPTY_ITEM_ERROR = 'Impossible d\'avoir un élement Vide'
DUPLICATE_ITEM_ERROR = "L'element existe déjà"
class ItemForm(forms.models.ModelForm):
	class Meta:
		model = Item
		fields = ('text',)
		widgets= {
			'text': forms.fields.TextInput(attrs={
			'placeholder': 'Enter a to-do item',
			'class': "form-control input-lg",
			}),
		}
		error_messages = {
			'text': {'required':EMPTY_ITEM_ERROR}
		}
	def save(self,for_list):
		self.instance.list = for_list
		return super().save()
class ExistingListItemForm(ItemForm):
	def __init__(self,for_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.list = for_list
	def save(self):
		return forms.models.ModelForm.save(self)
	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)
