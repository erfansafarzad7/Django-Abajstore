from django.urls import path,include
from django.contrib.auth.views import LogoutView
from . import views

app_name = "auth"

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="register"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('forget-password/', views.ForgetPasswordView.as_view(), name='forget_password'),

    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),

    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('address/<int:pk>/', views.AddressDetailView.as_view(), name='address_detail'),
    path('address/new/', views.AddressCreateView.as_view(), name='address_create'),
    path('address/<int:pk>/edit/', views.AddressUpdateView.as_view(), name='address_update'),
    path('address/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
]
