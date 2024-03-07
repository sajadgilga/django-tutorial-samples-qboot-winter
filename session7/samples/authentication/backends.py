from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from authentication.models import OTPCode


class OTPEmailAuthenticationBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if 'email' not in kwargs:
            return None
        email, code = kwargs['email'], kwargs['code']
        try:
            OTPCode.objects.get(code=code, email=email)
        except OTPCode.DoesNotExist:
            return None

        user = get_user_model().objects.get(email=email)
        return user
