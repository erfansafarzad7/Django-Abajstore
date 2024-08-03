from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:order_code>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('<int:order_code>/pay/', views.PayOrderView.as_view(), name='pay_order'),
    path('<int:order_code>/result/', views.PayOrderResultView.as_view(), name='pay_result'),

    # path('<int:order_id>/apply-coupon/', ApplyCouponView.as_view(), name='apply_coupon'),
    # path('<int:pk>/invoice/', OrderInvoiceView.as_view(), name='order_invoice'),
]
