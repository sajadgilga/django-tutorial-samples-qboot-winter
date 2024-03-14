from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=64)
    tags = models.CharField(max_length=256)
    description = models.TextField()
    published_date = models.DateTimeField(default=None, null=True)


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
