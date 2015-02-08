from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.forms import (
	ItemForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingListItemForm
	)
from lists.models import Item, List

from lists.views import home_page

class ListViewTest(TestCase):
	def test_for_invalid_input_renders_home_teplate(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		
	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))
	
	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertIsInstance(response.context['form'],ItemForm)
	
	def test_displays_item_form(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertIsInstance(response.context['form'], ExistingListItemForm)
		self.assertContains(response, 'name="text"')
		
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data = {'text': 'New Item on Existing List'}
			)
			
		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text,'New Item on Existing List')
		self.assertEqual(new_item.list, correct_list)
		
	def test_POST_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.post(
			'/lists/%d/' % (correct_list.id),
			data={'text': 'A new list Item'}
		)
		new_list = List.objects.last()
		self.assertRedirects(response,'/lists/%d/' % (correct_list.id,))
	
	def test_validation_errors_end_up_on_lists_pages(self):
		list_ = List.objects.create()
		response = self.client.post(
			'/lists/%d/' % (list_.id,),
			data = {'text': ''}
		)
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response, 'list.html')
		expected_error = escape("Impossible d'avoir un élement Vide")
		self.assertContains(response, expected_error)
		
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id),)
		self.assertEqual(response.context['list'],correct_list)
		
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response,'list.html')
		
	def test_displays_only_items_for_that_list(self):
		first_list = List.objects.create()
		Item.objects.create(text = 'item1',list=first_list)
		Item.objects.create(text = 'item2',list=first_list)
		second_list = List.objects.create()
		Item.objects.create(text = 'item3',list=second_list)
		Item.objects.create(text = 'item4',list=second_list)
		
		response = self.client.get('/lists/%d/' % (first_list.id,))
		
		self.assertContains(response,'item1')
		self.assertContains(response,'item2')
		self.assertNotContains(response,'item3')
		self.assertNotContains(response,'item4')
	def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
		list1 = List.objects.create()
		item1 = Item.objects.create(text = 'Am I Unique ?',list=list1)
		response = self.client.post(
		'/lists/%d/' % (list1.id,),
			data={'text': 'Am I Unique ?'}
		)
		self.assertContains(response, escape(DUPLICATE_ITEM_ERROR))
		self.assertTemplateUsed(response, 'list.html')
		self.assertEqual(Item.objects.all().count(),1)
		
class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'text': 'A new list Item'}
        )
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list Item')

	def test_redirects_after_POST(self):
		list_ = List.objects.create()
		response = self.client.post(
			'/lists/new',
			data={'text': 'A new list Item'}
        )
		new_list = List.objects.last()
		self.assertRedirects(response,'/lists/%d/' % (new_list.id,))
	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
	def test_for_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text':''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def post_invalid_input(self):
		list_ = List.objects.create()
		return self.client.post(
			'/lists/%d/' % (list_.id,),
			data={'text':''}
		)
	
	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'],ExistingListItemForm)
	
	def test_new_list_only_saves_item_when_necessary(self):
		self.client.post(
			'/lists/new',
			data={'item': ''}
		)
		self.assertEqual(Item.objects.count(), 0)	
		
		
class HomePageTest(TestCase):

	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
	
	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'],ItemForm)

	
		


