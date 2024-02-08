from django.contrib import admin

# Register your models here.
from posts.models import Post, Book


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
