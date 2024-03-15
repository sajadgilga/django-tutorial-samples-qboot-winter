from django.contrib import admin

# Register your models here.
from post.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_filter = ['created_date']
    search_fields = ['title', 'content', 'author__username']
