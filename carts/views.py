from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, DeleteView, RedirectView
from products.models import Product
from .forms import CartItemForm
from .models import Cart, CartItem


class CartItemCreateUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # product_id = request.POST.get('product_id')
        # product = get_object_or_404(Product, id=product_id)

        form = CartItemForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            quantity = cd['quantity']
            product = cd['product']
            # form.instance.product = product

            if product.quantity < int(quantity):
                # messages.error(self.request, 'تعداد درخواستی بیش از حد موجودی کالا است!')
                return redirect('products:product_detail', pk=product.id)

            try:
                cart, _ = Cart.objects.get_or_create(user=self.request.user)
                cart_item, created = CartItem.objects.update_or_create(cart=cart, product=product)

                cart_item.quantity = quantity
                cart_item.save()

                messages.success(self.request, 'محصول به سبد خرید اضافه شد!')
                return redirect('products:product_detail', pk=product.id)

            except Exception as e:
                messages.error(self.request, 'Something Wrong')

        return redirect('carts:all')
        # return HttpResponse("اطلاعات ارسال شده نامعتبر است!", status=400)
        # return super().post(request, *args, **kwargs)

# class CartItemCreateUpdateView(LoginRequiredMixin, CreateView):
#     model = CartItem
#     form_class = CartItemForm
#     template_name = 'cart/cart_item_form.html'
#     success_url = reverse_lazy('carts:all')
#
#     def form_valid(self, form):
#         product = form.cleaned_data['product']
#         quantity = form.cleaned_data['quantity']
#         color = form.cleaned_data['color']
#
#         if product.quantity < quantity:
#             messages.error(self.request, 'موجودی کافی نیست.')
#             return self.form_invalid(form)
#
#         try:
#             cart, created = Cart.objects.get_or_create(user=self.request.user)
#             cart_item, created = CartItem.objects.update_or_create(
#                 cart=cart,
#                 product=product,
#                 color=color,
#                 defaults={'quantity': quantity}
#             )
#             messages.success(self.request, 'سبد خرید با موفقیت به‌روز شد.')
#         except Exception as e:
#             messages.error(self.request, 'خطایی در به‌روزرسانی سبد خرید رخ داد.')
#             return self.form_invalid(form)
#
#         return super().form_valid(form)


class CartDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('pk')
        cart_item = get_object_or_404(CartItem, pk=cart_id)
        cart_item.delete()

        return redirect('carts:all')

# class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = CartItem
#     success_url = reverse_lazy('carts:all')
#
#     def test_func(self):
#         cart_item = self.get_object()
#         return cart_item.cart.user == self.request.user


class CartList(LoginRequiredMixin, TemplateView):
    template_name = 'carts/my-carts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['carts'] = cart.cart_items.all()
        context['cart'] = cart
        return context

# class CartList(LoginRequiredMixin, ListView):
#     model = CartItem
#     template_name = 'cart/cart_list.html'
#     context_object_name = 'cart_items'
#
#     def get_queryset(self):
#         cart, _ = Cart.objects.get_or_create(user=self.request.user)
#         return CartItem.objects.filter(cart=cart)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['cart'] = self.request.user.cart
#         return context


class UpdateCartItemQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item_id = request.POST.get('cartitem_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

        if action == 'increase':
            cart_item.quantity += 1
            if cart_item.product.quantity < cart_item.quantity:
                messages.error(request, 'تعداد درخواستی از مانده انبار بیشتر می باشد ')
                return redirect('carts:all')

        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                messages.error(request, 'تعداد نمی‌تواند کمتر از 1 باشد!')
                return redirect('carts:all')

        cart_item.save()

        return redirect('carts:all')
