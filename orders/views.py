from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from products.models import Product
from .models import Order, OrderItem
from .forms import CouponForm, OrderForm
from carts.models import Cart
import random


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/my-orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order-detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/checkout.html'
    success_url = reverse_lazy('order_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.address = self.request.user.address   # ---------------------------------------------<<<<<<<<
        order.code = str(random.randint(10**10, 10**15))
        order.save()

        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        cart_items = cart.cart_items.all()

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.cart_item_discounted_price(),
            )
            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.quantity
            product.save()
            item.delete()

        return redirect('orders:pay_order', kwargs={'order_id': order.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['carts'] = cart.cart_items.all()
        context['cart'] = cart
        return context


class ApplyCouponView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status != 'در انتظار پرداخت':
            messages.error(request, 'سفارش شما پرداخت شده است ، امکان اعمال کد تخفیف وجود ندارد')
            return redirect('order_detail', pk=order.id)

        form = CouponForm(request.POST)
        if form.is_valid():
            coupon = form.cleaned_data['coupon_code']
            order.coupon = coupon
            order.save()
            return redirect('order_detail', pk=order.id)
        return render(request, 'orders/apply-coupon.html', {'form': form, 'order': order})


class PayOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['order_id'], user=request.user)
        if order.status != 'در انتظار پرداخت':
            messages.error(request, f'سفارش شما {order.status}.')
            return redirect('order_detail', pk=order.id)

        # Here you would typically integrate with a payment gateway
        # For this example, we'll just mark the order as paid
        order.status = 'پرداخت شده'
        order.save()

        messages.success(request, 'سفارش شما با موفقیت پرداخت شد!')
        return redirect('order_detail', pk=order.id)


# class OrderInvoiceView(LoginRequiredMixin, DetailView):
#     model = Order
#     template_name = 'orders/invoice.html'
#     context_object_name = 'order'
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
