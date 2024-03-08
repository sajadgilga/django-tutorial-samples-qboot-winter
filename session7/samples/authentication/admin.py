from django.contrib import admin

# Register your models here.
from authentication.models import ImageUpload


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id',)
