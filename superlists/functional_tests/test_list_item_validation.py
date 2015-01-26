from .base import FunctionalTest
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
	def test_cannot_add_empty_list_item(self):
		#L'utilisateur arrive sur la page principale et essaye d'ajouter un item vide
		# il appuie sur entrÉ
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('\n')	
		
		#rafraichissement de la page principale avec un message d'erreur
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'Impossible d\'avoir un élement Vide')
		
		#L'utilisateur saisi maintenant une valeur correcte et appuie sur entré et ça fonctionne normalement
		self.get_item_input_box().send_keys('Acheter du pain\n')	
		self.check_for_row_in_list_table('1: Acheter du pain')
		
		# l'utilisateur essaye encore de saisir un champ vide
		self.get_item_input_box().send_keys('\n')
		
		# le même message d'erreur que a premiere fois est affiché
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'Impossible d\'avoir un élement Vide')
		
		# L'utilisateur saisie cette fois une valeur correcte
		self.get_item_input_box().send_keys('Acheter du vin\n')
		self.check_for_row_in_list_table('1: Acheter du pain')
		self.check_for_row_in_list_table('2: Acheter du vin')
			
		

