from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from order.models import Cart, CartItem, Order, OrderItem


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_pk):
        cart, _ = Cart.objects.get_or_create(archived=False, user=request.user)
        related_item = cart.items.filter(product_id=product_pk).first()
        if related_item:
            related_item.count += 1
        else:
            related_item = CartItem(product_id=product_pk, cart=cart)
        related_item.save()
        return JsonResponse({'message': 'Product was added to cart'})


class CartView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'cart_detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        cart = None
        try:
            cart = queryset.get(archived=False, user=self.request.user)
        except Cart.DoesNotExist:
            pass

        return cart

    @method_decorator(atomic)
    def post(self, request, *args, **kwargs):
        order = Order.objects.create(user=request.user)
        try:
            cart = Cart.objects.get(archived=False, user=request.user)
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'No active cart available'}, status=404)

        for item in cart.items.all():
            OrderItem.objects.create(product=item.product, order=order, count=item.count,
                                     price=item.product.get_price(request.user))

        cart.archived = True
        cart.save()

        return JsonResponse({'message': 'New order was successfully created'})
