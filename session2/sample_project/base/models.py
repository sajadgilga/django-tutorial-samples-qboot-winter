from django.db import models


# Create your models here.

def get_product_model():
    return 'order.Product'


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        draft = 0, 'draft'
        submitted = 1, 'submitted'
        rejected = 2, 'rejected'
        accepted = 3, 'accepted'

    complete = models.BooleanField(default=False, null=False)
    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.draft)
    info = models.OneToOneField(to='OrderInfo', on_delete=models.PROTECT)
    # Second method to implement many-to-many relation
    products = models.ManyToManyField(to=get_product_model(), through='order.ProductItem')
