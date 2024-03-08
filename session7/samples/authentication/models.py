from django.db import models


# Create your models here.

class OTPCode(models.Model):
    code = models.CharField(max_length=6)
    email = models.CharField(max_length=128)


class Book(models.Model):
    name = models.CharField(max_length=64)


class ImageUpload(models.Model):
    original_image = models.ImageField(upload_to='images')
    thumbnail_image = models.ImageField(upload_to='images/thumbnails', null=True, blank=True)
