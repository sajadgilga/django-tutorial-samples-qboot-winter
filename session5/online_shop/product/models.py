from django.core.files.storage import FileSystemStorage
from django.db import models

from authentication.models import UserType
from shared.models import BaseModel

product_fs = FileSystemStorage(location='static/products', base_url='/static/products')


class Product(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    image = models.ImageField(storage=product_fs)
    default_price = models.PositiveIntegerField()
    fellow_price = models.PositiveIntegerField(null=True)

    def get_price(self, user):
        if user.user_type == UserType.fellow:
            return self.fellow_price
        return self.default_price


class ProductProperty(BaseModel):
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=64)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='properties')
