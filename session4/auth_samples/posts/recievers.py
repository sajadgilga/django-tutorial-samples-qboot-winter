from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from authentication.models import user_creation_signal
from posts.models import MySender, Post, Comment


@receiver(user_creation_signal, sender=MySender)
def log_user_created(sender, *args, **kwargs):
    print("New user was created")
    print(sender, args, kwargs)


@receiver(post_save, sender=Post)
def create_first_comment(sender, instance, created, *args, **kwargs):
    if created:
        Comment.objects.create(text=f"first comment for post {instance.title}", post=instance)
    else:
        print(f"Post {instance.id} was edited")


@receiver(pre_save, sender=Comment)
def log_create_commment(sender, instance, *args, **kwargs):
    if instance.id:
        print(f"Comment {instance.id} was edited")
    else:
        print(f"Comment was created: {instance.text}")


@receiver(pre_save, sender=Post)
def update_title(sender, instance: Post, **kwargs):
    if instance.pk is not None:
        old_instance = Post.objects.get(pk=instance.pk)
        if instance.title != old_instance.title:
            instance.is_published = False

# Second way to register receiver to signal
# user_creation_signal.connect(log_user_created)
