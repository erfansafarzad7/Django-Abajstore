from django.db import models
from products.models import Product
import django_jalali.db.models as jmodels
from django.utils.translation import gettext as _
from accounts.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')

    created = jmodels.jDateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = jmodels.jDateField(_('تاریخ آپدیت'), auto_now=True)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید"

    def __str__(self):
        return f'سبد برای : {self.user}'

    def calculate_total_price(self):
        return sum(cart.cart_item_price() for cart in self.cart_items.all())

    def calculate_total_discounted_price(self):
        return sum(cart.cart_item_discounted_price() for cart in self.cart_items.all())

    def calculate_total_discount(self):
        return sum(cart.cart_item_discount() for cart in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items", verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, verbose_name='محصول')
    quantity = models.PositiveIntegerField(_('تعداد'), default=1)

    created = jmodels.jDateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = jmodels.jDateField(_('تاریخ آپدیت'), auto_now=True)

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم سبد خرید"

    def __str__(self):
        return f"{self.quantity} تا از {self.product}"

    def cart_item_price(self):
        return self.product.price * self.quantity

    def cart_item_discounted_price(self):
        return self.product.discounted_price * self.quantity

    def cart_item_discount(self):
        return (self.product.price * self.quantity) - (self.product.discounted_price * self.quantity)
