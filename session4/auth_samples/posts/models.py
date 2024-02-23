from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class ReadOnlyMixin:
    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise AttributeError("This object is read-only and cannot be saved.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise AttributeError("This object is read-only and cannot be deleted.")


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('can_publish', 'Can publish post'),
        )


class Article(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()


class Book(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()


class Image(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE)


class MySender:
    pass
