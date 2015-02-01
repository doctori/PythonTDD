from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from mock import patch
User = get_user_model()

@patch('accounts.views.authenticate')
class LoginViewTest(TestCase):

	def test_calls_authticate_with_assertion_from_post(
		self, mock_authenticate
	):
		mock_authenticate.return_value = None
		self.client.post('/accounts/login',{'assertion':'assert this'})
		mock_authenticate.assert_called_once_with(assertion='assert this')
	
	def test_returns_OK_when_user_found(
		self, mock_authenticate
	):
		user = User.objects.create(email='dummy@pouet.com')
		user.backend = ''
		mock_authenticate.return_value = user
		response = self.client.post('/accounts/login',{'assertion':'a'})
		self.assertEqual(response.content.decode(), 'OK')
		
	def test_gets_loggedin_if_auth_return_a_user(
		self, mock_authenticate
	):
		user = User.objects.create(email='dummy@pouet.com')
		user.backend = ''
		mock_authenticate.return_value = user
		response = self.client.post('/accounts/login',{'assertion':'a'})
		self.assertEqual(self.client.session[SESSION_KEY], user.pk)
		
	def test_does_not_gets_loggedin_if_auth_return_None(
		self, mock_authenticate
	):
		mock_authenticate.return_value = None
		response = self.client.post('/accounts/login',{'assertion':'a'})
		self.assertNotIn(SESSION_KEY, self.client.session)
	
