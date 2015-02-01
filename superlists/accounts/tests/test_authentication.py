from django.test import TestCase
from mock import patch

from accounts.authentication import (
	PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)

@patch('accounts.authentication.requests.post')
class testAuthentication(TestCase):

	def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
		backend = PersonaAuthenticationBackend()
		backend.authenticate('assert this')
		mock_post.assert_called_once_with(
			PERSONA_VERIFY_URL,
			data={'assertion':'assert this','audience':DOMAIN}
		)

	def test_returns_none_if_response_error(self, mock_post):
		mock_post.return_value.ok = False
		backend = PersonaAuthenticationBackend()
		user = backend.authenticate('assert this')
		self.assertIsNone(user)
