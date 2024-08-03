from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse

from products.models import Product
from .models import Order, OrderItem
from .forms import CouponForm, OrderForm
from carts.models import Cart
import random


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/my-orders.html'
    context_object_name = 'orders'
    paginate_by = 3     # ---------------------------------------------------<<<<<<<<<<<<<<<<<<<<<<

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order-detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        return Order.objects.get(code=self.kwargs['order_code'])


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/checkout.html'
    success_url = reverse_lazy('orders:order_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        random_code = str(random.randint(10**10, 10**15))
        order = form.save(commit=False)
        order.user = self.request.user
        order.code = random_code
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
            item.delete()

        # pay_order_url = reverse('orders:pay_order', kwargs={'order_code': random_code})
        return redirect('orders:pay_order', order_code=random_code)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['carts'] = cart.cart_items.all()
        context['cart'] = cart
        return context


# class ApplyCouponView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         order_code = self.kwargs['order_code']
#         order = get_object_or_404(Order, code__exact=order_code, user=request.user)
#         if order.status != 'در انتظار پرداخت':
#             messages.error(request, 'سفارش شما پرداخت شده است ، امکان اعمال کد تخفیف وجود ندارد')
#             return redirect('orders:order_detail', code=order_code)
#
#         form = CouponForm(request.POST)
#         if form.is_valid():
#             coupon = form.cleaned_data['coupon_code']
#             order.coupon = coupon
#             order.save()
#             return redirect('orders:order_detail', code=order_code)
#         return render(request, 'orders/apply-coupon.html', {'form': form, 'order': order})


class PayOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_code = self.kwargs['order_code']
        order = get_object_or_404(Order, code__exact=order_code, user=request.user)
        if order.status != 'در انتظار پرداخت':
            messages.error(request, f'سفارش شما {order.status}.')
            return redirect('orders:order_detail', order_code=order_code)

        print(order.get_price())
        print(order.code)
        order.status = 'پرداخت شده'
        order.save()
        # send to dargah with code

        return redirect('orders:pay_result', order_code=order_code)


class PayOrderResultView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/pay-result.html'

    def get_object(self, order_code):
        return get_object_or_404(Order, code__exact=order_code, user=self.request.user)

    def get(self, request, *args, **kwargs):
        order_code = self.kwargs['order_code']
        # order = get_object_or_404(Order, code__exact=order_code, user=request.user)
        order = self.get_object(order_code)

        # receive pay code and check if done set to paid else canceled
        # order.status = 'پرداخت شده' - 'در انتظار پرداخت '
        # order.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_code = self.kwargs['order_code']
        # order = get_object_or_404(Order, code__exact=order_code, user=self.request.user)
        order = self.get_object(order_code)
        context['order'] = order
        return context


# class OrderInvoiceView(LoginRequiredMixin, DetailView):
#     model = Order
#     template_name = 'orders/invoice.html'
#     context_object_name = 'order'
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
