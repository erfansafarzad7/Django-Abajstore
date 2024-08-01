from django import forms
from products.models import Product
from .models import CartItem


class CartItemForm(forms.ModelForm):
    quantity = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'bg-[transparent] text-center w-full outline-none',
                                      'placeholder': '1',
                                      'value': '1'}),
    )

    class Meta:
        model = CartItem
        fields = ('quantity',)

    # def validate_quantity(self, value):
    #     print(value)
    #     if int(value) > self.product.quantity:
    #         raise forms.ValidationError('تعداد بیش از حد موجودی است!')
    #     return value
