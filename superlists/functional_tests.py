from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)	
	
	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		#acces a la page de garde
		self.browser.get('http://localhost:8000')
		# le titre de la page est 'To-Do' et le titre sur la page
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		# L'utilisateur est incvité a saisir une action 'To-Do'
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		# L'utilisateur saisi "Acheter du mortier"
		inputbox.send_keys('Acheter du mortier')
		#Après a voir saisi l'element et appuyé sur ENTRER la page se met a jout et la page liste l'item
		inputbox.send_keys(Keys.ENTER)
		
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Acheter du mortier' for row in rows),
			" New To-Do Item did not appear in table"
		)
		#Il reste un champ de saisie pour ajouter un item
		# L'utilisateur y ajoute "Faire un mur"
		self.fail('Finish the Test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')
