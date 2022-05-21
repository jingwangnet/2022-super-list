from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from accounts.models import Token

User = get_user_model()

class PasswordlessAuthenticationBackend(BaseBackend):

    def authenticate(self, request=None, uid=None):
        try: 
            token = Token.objects.get(uid=uid)
            user = User.objects.get(email=token.email)
            return user
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            user = User.objects.create(email=token.email)
            return user

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
