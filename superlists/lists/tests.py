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
		
		
class ListViewTest(TestCase):
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/', % (list_.id,))
		self.assertTemplateUsed(response,'list.html')
		
	def test_displays_all_list_items(self):
		list_ = List.objects.create()
		Item.objects.create(text = 'item1',list=list_)
		Item.objects.create(text = 'item2',list=list_)
		
		response = self.client.get('/lists/%d/', % (list_id,))
		
		self.assertContains(response,'item1')
		self.assertContains(response,'item2')
		
		
class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list Item'}
        )
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list Item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list Item'}
        )
		self.assertRedirects(response,'/lists/unique-list-name/')
	
	def test_new_list_only_saves_item_when_necessary(self):
		self.client.post(
			'/lists/new',
			data={'item_text': ''}
		)
		self.assertEqual(Item.objects.count(), 0)	
		
		
class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
	
	
		


