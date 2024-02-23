from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models

user_fs = FileSystemStorage(location='static/users')


class UserType(models.TextChoices):
    normal = 'normal', 'Normal User'
    fellow = 'fellow', 'Fellow User'
    warehouse = 'warehouse', 'Warehouse Admin'
    finance = 'finance', 'Finance Admin'
    super = 'super', 'Super Admin'


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11)
    user_type = models.CharField(max_length=16, choices=UserType.choices, default=UserType.normal)
    fellow_document = models.FileField(storage=user_fs, null=True, blank=True)
