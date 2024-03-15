from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
