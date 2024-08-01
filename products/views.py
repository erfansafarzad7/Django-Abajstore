from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import django_filters
from django_filters.views import FilterView
from .models import Product, MainCategory
from carts.forms import CartItemForm


# class ProductFilter(django_filters.FilterSet):
#     class Meta:
#         model = Product
#         fields = {
#             'name': ['exact', 'icontains'],
#             'brand': ['exact', 'icontains'],
#             'category': ['exact'],
#             'colors': ['exact'],
#             'price': ['gte', 'lte'],
#             'discount': ['gte', 'lte'],
#             'avg_rate': ['gte', 'lte'],
#             'created': ['gte', 'lte'],
#         }


# /products/?name=product1&brand__icontains=brand1&price__gte=1000&price__lte=5000&ordering=price


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(queryset=MainCategory.objects.all())
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='حداقل قیمت')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='حداکثر قیمت')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('created', 'created'),
            ('price', 'price'),
            ('discount', 'discount'),
            # ('avg_rate', 'avg_rate'),
        )
    )

    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'price_min', 'price_max']


class HomeView(TemplateView):
    template_name = 'products/home.html'


class ProductListView(FilterView):
    model = Product
    template_name = 'products/all-products.html'
    context_object_name = 'products'
    paginate_by = 20
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.available.all().order_by('-created')

    # def get_queryset(self):
    #     queryset = Product.available.all().order_by('-created')
    #     filterset = self.filterset_class(self.request.GET, queryset=queryset)
    #     return filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
    #     return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartItemForm()
        return context
