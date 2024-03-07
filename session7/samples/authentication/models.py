from django.db import models


# Create your models here.

class OTPCode(models.Model):
    code = models.CharField(max_length=6)
    email = models.CharField(max_length=128)
