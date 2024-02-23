from django.db.models import F
from django.views import View
from django.views.generic import ListView, DetailView

from authentication.models import UserType
from product.models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        is_fellow = self.request.user.is_authenticated and self.request.user.user_type == UserType.fellow

        if is_fellow:
            queryset = queryset.annotate(price=F('fellow_price'))
        else:
            queryset = queryset.annotate(price=F('default_price'))
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = self.object.properties.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        is_fellow = self.request.user.is_authenticated and self.request.user.user_type == UserType.fellow

        if is_fellow:
            queryset = queryset.annotate(price=F('fellow_price'))
        else:
            queryset = queryset.annotate(price=F('default_price'))
        return queryset

