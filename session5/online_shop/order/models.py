from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from shared.models import BaseModel


class Cart(BaseModel):
    name = models.CharField(max_length=16, null=True, blank=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    def clean(self):
        if Cart.objects.filter(archived=False, user=self.user).count() > 1:
            raise ValidationError('There should not be more than 2 active carts for each user')


class CartItem(BaseModel):
    cart = models.ForeignKey(to='Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(to='product.Product', on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=1)


class OrderStatus(models.TextChoices):
    in_progress = 'in_progress', 'order in progress'
    warehouse = 'warehouse', 'warehouse check'
    delivery = 'delivery', 'order to be delivered'
    finished = 'finished', 'order received'
    cancelled = 'cancelled', 'order cancelled'


class Order(BaseModel):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=OrderStatus.choices, default=OrderStatus.in_progress)

    @property
    def total_price(self):
        return self.items.aggregate(total_price=Sum('price'))


class OrderItem(BaseModel):
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(to='product.Product', on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveIntegerField()
