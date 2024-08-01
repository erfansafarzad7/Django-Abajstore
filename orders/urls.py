# from django.urls import path
# from . import views
#
# app_name = 'order'
# urlpatterns = [
#     path('', views.OrderListView.as_view(), name='order_list'),
#     path('create/', views.OrderCreateView.as_view(), name='order_create'),
#     path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
#     path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
#     path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
#     path('<int:pk>/apply-coupon/', views.apply_coupon, name='apply_coupon'),
#     path('<int:pk>/pay/', views.pay_order, name='pay_order'),
# ]
# ============================================================================================================
from django.urls import path
from .views import *

app_name = 'orders'
urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path('<int:order_id>/apply-coupon/', ApplyCouponView.as_view(), name='apply_coupon'),
    path('<int:order_id>/pay/', PayOrderView.as_view(), name='pay_order'),
    # path('<int:pk>/invoice/', OrderInvoiceView.as_view(), name='order_invoice'),
]
