from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'status', 'get_price', 'created']
    list_filter = ['status', 'created']
    inlines = [OrderItemInline]
    readonly_fields = ['get_price', 'code']

    def get_price(self, obj):
        return obj.get_price()
    get_price.short_description = 'قیمت کل'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'value', 'valid_until', 'active']
    list_filter = ['active', 'valid_until']
