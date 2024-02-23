from django.contrib import admin

# Register your models here.
from product.models import Product, ProductProperty


class ProductPropertyInlineAdmin(admin.TabularInline):
    extra = 1
    model = ProductProperty
    fields = ('name', 'value', 'archived')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'default_price', 'fellow_price')
    list_filter = ('created_date', 'archived')
    search_fields = ('name',)
    inlines = (ProductPropertyInlineAdmin,)
