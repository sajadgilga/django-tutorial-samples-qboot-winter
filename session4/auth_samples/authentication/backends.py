from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # if we want to signup user if not registered already
            # user = User.objects.create_user(username=email, email=email, password=password)
            return None
        if user.check_password(password):
            return user
