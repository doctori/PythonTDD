from django.core.urlresolvers import resolve
from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

from lists.views import home_page

class ListAndItemModelsTest(TestCase):
	def test_default_text(self):
		item = Item()
		self.assertEqual(item.text, '')
	def test_item_is_related_to_list(self):
		list_ = List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		self.assertIn(item, list_.item_set.all())
	def test_cannot_save_empty_list_item(self):
		list_ = List.objects.create()
		item = Item(list=list_,text='')
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()
	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))
	def test_duplicate_items_are_invalid(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='Am I Unique ?')
		with self.assertRaises(ValidationError):
			item = Item(list=list_, text='Am I Unique ?')
			item.full_clean()
	def test_CAN_save_item_to_different_lists(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='Am I Unique ?')
		item = Item(list=list2, text='Am I Unique ?')
		item.full_clean() #Should pass
	def test_list_ordering(self):
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='Am I The First ?')
		item2 = Item.objects.create(list=list1, text='1 and Only')
		item3 = Item.objects.create(list=list1, text='Z I\'m always the last')
		self.assertEqual(
			list(Item.objects.all()),
			[item1,item2,item3]
		)
	def test_string_representation(self):
		item = Item(text='Am I readable ?')
		self.assertEqual(str(item),'Am I readable ?')
		

