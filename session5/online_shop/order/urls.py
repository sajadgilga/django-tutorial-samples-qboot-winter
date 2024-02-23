from django.urls import path

from order.views import CartAddView, CartView

urlpatterns = [
    path('cart/add/<int:product_pk>/', CartAddView.as_view(), name='cart_add_view'),
    path('cart/', CartView.as_view(), name='cart_view'),
]
