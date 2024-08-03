from django.db import models
from products.models import Product
import django_jalali.db.models as jmodels
from django.utils.translation import gettext as _
from accounts.models import User, Address


class Coupon(models.Model):
    code = models.CharField(_('کد'), max_length=30, unique=True)
    value = models.PositiveSmallIntegerField(_('مقدار'), help_text=_('مقدار تخفیف به درصد'))
    # valid_from = jmodels.jDateField()
    valid_until = jmodels.jDateField(_('معتبر تا تاریخ'), )
    active = models.BooleanField(_('فعال'), default=True)

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد تخفیف"

    def __str__(self):
        return self.code


class Order(models.Model):
    ORDER_STATUS = [
        ("در انتظار پرداخت", _("در انتظار پرداخت")),
        ("پرداخت شده", _("پرداخت شده")),
        ("ارسال شده", _("ارسال شده")),
        ("تحویل داده شده", _("تحویل داده شده")),
        ("لغو شده", _("لغو شده")),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    code = models.CharField(_('کد سفارش'), max_length=15, unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='آدرس')
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='')
    send_price = models.PositiveIntegerField(_('هزینه ی ارسال'), default=30_000)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True, blank=True, verbose_name='کد تخفیف')
    status = models.CharField(_('وضعیت'), max_length=20, choices=ORDER_STATUS, default='در انتظار پرداخت')

    created = jmodels.jDateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = jmodels.jDateTimeField(_('تاریخ آپدیت'), auto_now=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return str(self.code)

    def get_price(self):
        if self.order_items:
            total_price = sum(item.price for item in self.order_items.all())

            if self.coupon:
                return total_price - (total_price * (self.coupon.value / 100))

            return total_price
        return 0

    def get_price_with_send(self):
        return int(self.get_price() + self.send_price)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='محصول')
    # color = models.CharField(_('رنگ'), max_length=20, null=True, blank=True)
    # size = models.CharField(_('سایز'), max_length=20, null=True, blank=True)
    quantity = models.PositiveIntegerField(_('تعداد'), default=1)
    price = models.PositiveIntegerField(_('جمع قیمت (محاسبه شده با تعداد)'), )

    created = jmodels.jDateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = jmodels.jDateTimeField(_('تاریخ آپدیت'), auto_now=True)

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم سفارش"

    def __str__(self):
        return str(self.order)
