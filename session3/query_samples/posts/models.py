from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(archived=False)


class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    engagement_count = models.PositiveIntegerField()
    templates = models.ManyToManyField(to='PostTemplate', related_name='posts')
    archived = models.BooleanField(default=False)

    # not_archived = PostManager()


class Comment(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='my_comments')


class PostTemplate(models.Model):
    title_template = models.CharField(max_length=64)
    content_template = models.TextField()

    def __str__(self):
        return f"title: {self.title_template}"


class Library(models.Model):
    name = models.CharField(max_length=32)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


def default_library():
    lib = Library.objects.first()
    if not lib:
        lib = Library.objects.create(name='default library')
    return lib


class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True)
    archived = models.BooleanField(default=False)
    library = models.ForeignKey(to=Library, on_delete=models.CASCADE, default=default_library)
    tags = models.TextField(null=True)
