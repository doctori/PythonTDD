from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
	def test_can_start_a_list_and_retrieve_it_later(self):
		#acces a la page de garde
		self.browser.get(self.server_url)
		# le titre de la page est 'To-Do' et le titre sur la page
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		#le champ de saisi est bien centré
		# L'utilisateur est invité a saisir une action 'To-Do'
		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		# L'utilisateur saisi "Acheter du mortier"
		inputbox.send_keys('Acheter du mortier')
		#Après a voir saisi l'element et appuyé sur ENTRER la page se met a jout et la page liste l'item
		inputbox.send_keys(Keys.ENTER)
		#On doit arriver sur la liste complete de l'utilisateur 
		user1_list_url = self.browser.current_url
		self.assertRegex(user1_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Acheter du mortier')
				
		#Il reste un champ de saisie pour ajouter un item
		# L'utilisateur y ajoute "Faire un mur"
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Faire un mur')
		inputbox.send_keys(Keys.ENTER)		
		self.check_for_row_in_list_table('1: Acheter du mortier')
		self.check_for_row_in_list_table('2: Faire un mur')
		
		#On veux vérifier qu'un autre utilisateur (user2) n'accede pas a la liste du user1
		self.browser.quit()
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)	
		#user2 Visite la page d'accueil
		self.browser.get(self.server_url)
		# pas de traces des enregistrement du user1 
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Acheter du mortier',page_text)
		self.assertNotIn('Faire un mur',page_text)
		
		#user2 démare une nouvelle liste 
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Acheter des raisins')
		inputbox.send_keys(Keys.ENTER)
		#On doit arriver sur la liste complete de l'utilisateur 
		user2_list_url = self.browser.current_url
		self.assertRegex(user2_list_url, '/lists/.+')
		self.assertNotEqual(user1_list_url,user2_list_url)
		# pas de traces des enregistrement du user1 
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Acheter du mortier',page_text)
		self.assertNotIn('Faire un mur',page_text)
		self.check_for_row_in_list_table('1: Acheter des raisins')

