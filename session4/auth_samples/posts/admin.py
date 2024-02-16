from django.contrib import admin

# Register your models here.
from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id']
