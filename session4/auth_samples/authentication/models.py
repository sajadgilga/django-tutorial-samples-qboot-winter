from datetime import datetime, timedelta

import jwt
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal

from auth_samples.settings import TOKEN_EXPIRE_TIME, TOKEN_DATE_FORMAT

user_creation_signal = Signal()


# Create your models here.

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11)


class TokenManager(models.Manager):
    def generate_token(self, user):
        expire_time = datetime.now() + timedelta(seconds=TOKEN_EXPIRE_TIME)
        token = jwt.encode({
            'username': user.username,
            'user_id': user.id,
            'full_name': user.get_full_name(),
            'email': user.email,
            'expire_time': expire_time.strftime(TOKEN_DATE_FORMAT)
        }, SECRET_KEY)
        # store token
        self.create(token=token, user=user)
        return token


class Token(models.Model):
    user = models.ForeignKey(to="CustomUser", on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    objects = TokenManager()
