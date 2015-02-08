from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest

class MyListsTest(FunctionalTest):
	
	def create_pre_authenticated_session(self,email):
		user = User.objects.create(email=email)
		session = SessionStore()
		session[SESSION_KEY] = user.pk
		session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		session.save()
		#Creation d'un cookie en passant sur une page 404 (plus rapide)
		self.browser.get(self.server_url + "/404_pouet_pouet")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session.session_key,
			path="/",
		))
		
