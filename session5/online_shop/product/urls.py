from django.urls import path

from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_view'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail_view'),
]
