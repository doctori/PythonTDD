from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from django.conf import settings
from mock import patch
User = get_user_model()

from accounts.authentication import (
	PERSONA_VERIFY_URL,PersonaAuthenticationBackend
)

@patch('accounts.authentication.requests.post')
class testAuthentication(TestCase):

	def setUp(self):
		self.backend = PersonaAuthenticationBackend()
		user = User(email='PrimalDummy@NSA.com')
		user.username = 'Sir Dummy'
		user.save()
		
	def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
		self.backend.authenticate('assert this')
		mock_post.assert_called_once_with(
			PERSONA_VERIFY_URL,
			data={'assertion':'assert this','audience':settings.DOMAIN}
		)

	def test_returns_none_if_response_error(self, mock_post):
		mock_post.return_value.ok = False
		mock_post.return_value.json.return_value = {}
		user = self.backend.authenticate('assert this')
		self.assertIsNone(user)
	
	def test_returns_none_if_status_not_okay(self, mock_post):
		mock_post.return_value.json.return_value = {'status': 'not okay!'}
		user = self.backend.authenticate('assert this')
		self.assertIsNone(user)


	def test_finds_existing_user_with_email(self, mock_post):
		mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'dummy@pouet.com'}
		actual_user = User.objects.create(email='dummy@pouet.com')
		found_user = self.backend.authenticate('assert this')
		self.assertEqual(found_user, actual_user)
	def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
		mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'dummy@pouet.com'}
		found_user = self.backend.authenticate('assert this')
		new_user = User.objects.get(email='dummy@pouet.com')
		self.assertEqual(found_user, new_user)

class GetUserTest(TestCase):
	def test_gets_user_by_email(self):
		backend = PersonaAuthenticationBackend()
		other_user = User(email='DummyTwo@pouet.com')
		other_user.username = 'DummyTwo'
		other_user.save()
		desired_user = User.objects.create(email='DummyOne@pouet.com')
		found_user = backend.get_user('DummyOne@pouet.com')
		self.assertEqual(found_user, desired_user)

	def test_returns_none_if_no_user_with_that_email(self):
		backend = PersonaAuthenticationBackend()
		self.assertIsNone(
		backend.get_user('DummyOne@pouet.com')
)

