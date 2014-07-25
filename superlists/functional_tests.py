from selenium import webdriver
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
		# le titre de la page est 'To-Do'
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the Test')
if __name__ == '__main__':
	unittest.main(warnings='ignore')
