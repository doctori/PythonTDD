from django.test import TestCase
from mock import patch

from accounts.authentication import (
	PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)
class testAuthentication(TestCase):

	@patch('accounts.authentication.requests.post')
	def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
		backend = PersonaAuthenticationBackend()
		backend.authenticate('assert this')
		mock_post.assert_called_once_with(
			PERSONA_VERIFY_URL,
			data={'assertion':'assert this','audience':DOMAIN}
		)
