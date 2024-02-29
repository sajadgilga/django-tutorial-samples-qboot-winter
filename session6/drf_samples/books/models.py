from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    published_date = models.DateField(null=True, blank=True)

    @property
    def info(self):
        return self.title + ': ' + self.description


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
