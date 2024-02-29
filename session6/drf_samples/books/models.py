from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=32)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    published_date = models.DateField(null=True, blank=True)
