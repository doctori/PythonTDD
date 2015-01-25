from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List

from lists.views import home_page

class ListAndItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()
		
		first_item = Item()
		first_item.text = 'First List Item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Second List Item'
		second_item.list = list_
		second_item.save()
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text,'First List Item')
		self.assertEqual(first_saved_item.list,list_)
		
		self.assertEqual(second_saved_item.text,'Second List Item')
		self.assertEqual(second_saved_item.list,list_)
		

