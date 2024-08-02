from django import forms
from .models import Order, Coupon
from accounts.models import Address


class CouponForm(forms.Form):
    coupon_code = forms.CharField(max_length=50)

    def clean_coupon_code(self):
        code = self.cleaned_data['coupon_code']
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            if not coupon.is_valid():
                raise forms.ValidationError('کد تخفیف منقضی شده است!')
            return coupon
        except Coupon.DoesNotExist:
            raise forms.ValidationError('کد تخفیف نامعتبر است!')


class OrderForm(forms.ModelForm):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=True,
        label='آدرس',
        empty_label=None
    )

    class Meta:
        model = Order
        fields = ['address', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user=user)

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         self.fields['address'].queryset = Address.objects.filter(user=user)
    #         self.fields['address'].widget.attrs.update({
    #             'class': 'form-control',
    #             'placeholder': 'انتخاب آدرس'
    #         })