from django.contrib import admin

# Register your models here.
from order.models import Cart, CartItem, OrderItem, Order


class CartItemInlineAdmin(admin.TabularInline):
    extra = 1
    model = CartItem
    fields = ('product', 'count', 'archived')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_date', 'archived')
    list_filter = ('archived', 'created_date',)
    inlines = (CartItemInlineAdmin,)


class OrderItemInlineAdmin(admin.TabularInline):
    extra = 1
    model = OrderItem
    fields = ('product', 'count', 'price', 'archived')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_date', 'archived')
    list_filter = ('archived', 'status', 'created_date',)
    inlines = (OrderItemInlineAdmin,)
