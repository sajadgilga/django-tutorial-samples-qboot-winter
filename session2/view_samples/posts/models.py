from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=64, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    release_date = models.DateTimeField(null=True)
    accepted = models.BooleanField(default=False)


class Comment(models.Model):
    class CommentStatus(models.TextChoices):
        draft = 'draft', 'Draft'
        accepted = 'accepted', 'Accepted'
        rejected = 'rejected', 'Rejected'

    text = models.CharField(max_length=512, null=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    status = models.CharField(choices=CommentStatus.choices, default=CommentStatus.draft, max_length=9)
