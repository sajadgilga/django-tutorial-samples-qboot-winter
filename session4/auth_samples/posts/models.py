from django.contrib.auth import get_user_model
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
