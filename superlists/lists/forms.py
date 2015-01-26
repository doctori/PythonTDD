from django import forms
from lists.models import Item, List

EMPTY_ITEM_ERROR = 'Impossible d\'avoir un élement Vide'
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
