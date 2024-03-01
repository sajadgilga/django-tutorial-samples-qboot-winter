from django.contrib.auth import get_user_model
from django.db import models


class BookStateLogic:
    def publish(self, obj):
        pass

    def reject(self, obj):
        pass

    def notify_users(self, obj):
        pass


class BookDraft(BookStateLogic):
    def publish(self, obj):
        obj.state = BookState.moderation
        obj.save()

    def reject(self, obj):
        raise Exception('You cannot reject book in draft state')

    def notify_users(self, obj):
        pass


class BookModeration(BookStateLogic):
    def publish(self, obj):
        obj.state = BookState.published
        obj.save()

    def reject(self, obj):
        obj.state = BookState.draft
        obj.save()

    def notify_users(self, obj):
        pass


class BookPublished(BookStateLogic):
    def publish(self, obj):
        obj.state = BookState.published
        obj.save()

    def reject(self, obj):
        obj.state = BookState.draft
        obj.save()

    def notify_users(self, obj):
        pass


class BookState(models.TextChoices):
    draft = 'draft', 'Draft'
    moderation = 'moderation', 'Moderation'
    published = 'published', 'Published'
    editing = 'editing', "Editing"


class Book(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    published_date = models.DateField(null=True, blank=True)
    archive = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    state = models.CharField(choices=BookState.choices, max_length=16)

    @property
    def info(self):
        return self.title + ': ' + self.description

    @property
    def state_class(self) -> BookStateLogic:
        state_mapping = {
            BookState.draft: BookDraft(),
            BookState.moderation: BookModeration(),
            BookState.editing: BookModeration(),
            BookState.published: BookPublished()
        }
        return state_mapping[self.state]

    def publish(self):
        self.state_class.publish(self)

    def reject(self):
        self.state_class.reject(self)

    def notify_users(self):
        self.state_class.notify_users(self)


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(to='Book', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    tag = models.CharField(max_length=16)


class Company(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    created_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    size = models.PositiveSmallIntegerField()
    field = models.CharField(max_length=64)

    @property
    def date(self):
        return self.created_date if self.is_active else self.end_date


class Department(models.Model):
    director = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='departments')
    members = models.ManyToManyField(get_user_model(), related_name='departments')
