from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from utils.validators import persian_phone_number_validation
from .models import User, OTP, Address


class UserCreationForm(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'border-submitPageColorBorderLowBlack border-2 w-full py-2 px-2 outline-none focus:border-submitPageColorBorderBlue transition-all',
                                      'placeholder': 'شماره موبایل'}),
        error_messages={
            'required': 'لطفا شماره موبایل خود را وارد کنید.',
            'invalid': 'کاربری با این شماره یافت نشد.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'border-submitPageColorBorderLowBlack border-2 w-full py-2 px-2 outline-none focus:border-submitPageColorBorderBlue transition-all',
                                          'placeholder': 'رمز عبور'}),
        error_messages={
            'required': 'لطفا گذرواژه خود را وارد کنید.',
            'invalid': 'گذرواژه وارد شده صحیح نیست.',
        }
    )

    class Meta:
        model = User
        fields = ('phone_number', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'border-submitPageColorBorderLowBlack border-2 w-full py-2 px-2 outline-none focus:border-submitPageColorBorderBlue transition-all',
                                      'placeholder': 'شماره موبایل'}),
        error_messages={
            'required': 'لطفا شماره موبایل خود را وارد کنید.',
            'invalid': 'کاربری با این شماره یافت نشد.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'border-submitPageColorBorderLowBlack border-2 w-full py-2 px-2 outline-none focus:border-submitPageColorBorderBlue transition-all',
                                          'placeholder': 'رمز عبور'}),
        error_messages={
            'required': 'لطفا گذرواژه خود را وارد کنید.',
            'invalid': 'گذرواژه وارد شده صحیح نیست.',
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'شماره موبایل یا رمز اشتباه است!'
        self.fields['username'].error_messages = {'required': 'شماره موبایل را وارد کنید'}
        self.fields['password'].error_messages = {'required': 'رمز عبور را وارد کنید'}


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text=
                                         "برای تغییر گذرواژه  <a href=\"../password/\"> وارد شوید </a>.")

    class Meta:
        model = User
        fields = '__all__'


class ForgetPasswordForm(forms.Form):
    phone_number = forms.CharField(max_length=11, validators=[persian_phone_number_validation, ], label='شماره موبایل',
                                   widget=forms.TextInput(attrs={
                                       'class': 'border-submitPageColorBorderLowBlack border-2 w-full py-2 px-2 '
                                                'outline-none focus:border-submitPageColorBorderBlue transition-all',
                                       'placeholder': '09123456789'
                                   }))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            User.objects.get(phone_number__exact=phone_number)
        except User.DoesNotExist:
            raise forms.ValidationError('کاربری با این شماره یافت نشد!')

        return phone_number


class OTPForm(forms.Form):
    code = forms.CharField(max_length=5,
                           widget=forms.TextInput(attrs={
                                   'class': 'border-submitPageColorBorderLowBlack border-2 w-full py-2 px-2'
                                            ' outline-none focus:border-submitPageColorBorderBlue transition-all',
                                   'placeholder': 'کد تایید 5 رقمی'
                               }))

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit() or len(code) != 5:
            raise forms.ValidationError('کد را فقط به صورت عددی و به لاتین وارد کنید')

        try:
            OTP.objects.get(code=code)
        except OTP.DoesNotExist:
            raise forms.ValidationError('کد وارد شده اشتباه است!')

        return code


#
# class ChangePasswordForm(SetPasswordForm):
#     old_password = forms.CharField(
#         label=_("رمز عبور فعلی"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
#     )
#
#     def clean_old_password(self):
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise ValidationError(
#                 _("رمز عبور فعلی شما نادرست است. لطفاً دوباره وارد کنید."),
#                 code='password_incorrect',
#             )
#         return old_password
#
#
# class ChangePhoneNumberForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['phone_number']
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#
#     def clean_phone_number(self):
#         phone_number = self.cleaned_data['phone_number']
#         if User.objects.filter(phone_number=phone_number).exclude(pk=self.user.pk).exists():
#             raise ValidationError(_("این شماره موبایل قبلاً ثبت شده است."))
#         return phone_number
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'outline-none px-2 py-3 rounded border-2'
                                               ' border-submitPageColorBorderLowBlack focus:border-2'
                                               ' focus:border-submitPageColorBorderBlue',
                                      'placeholder': 'نام'}),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'outline-none px-2 py-3 rounded border-2 '
                                               'border-submitPageColorBorderLowBlack focus:border-2 '
                                               'focus:border-submitPageColorBorderBlue',
                                      'placeholder': 'نام خانوادگی'}),
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'outline-none px-2 py-3 rounded border-2'
                                               ' border-submitPageColorBorderLowBlack focus:border-2 '
                                               'focus:border-submitPageColorBorderBlue',
                                      'placeholder': 'شماره موبایل'}),
    )
    card_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'outline-none px-2 py-3 rounded border-2 '
                                               'border-submitPageColorBorderLowBlack focus:border-2'
                                               ' focus:border-submitPageColorBorderBlue',
                                      'placeholder': 'شماره کارت'}),
    )
    shaba_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'outline-none px-2 py-3 rounded border-2 '
                                               'border-submitPageColorBorderLowBlack focus:border-2 '
                                               'focus:border-submitPageColorBorderBlue',
                                      'placeholder': 'شماره شبا'}),
    )

    current_password = forms.CharField(label='رمز فعلی', widget=forms.PasswordInput(
        attrs={'class': 'outline-none px-2 py-3 rounded border-2 border-submitPageColorBorderLowBlack '
                        'focus:border-2 focus:border-submitPageColorBorderBlue',
               'placeholder': 'رمز فعلی'}), required=True)

    password = forms.CharField(label='رمز جدید', widget=forms.PasswordInput(
        attrs={'class': 'outline-none px-2 py-3 rounded border-2 border-submitPageColorBorderLowBlack'
                        'focus:border-2 focus:border-submitPageColorBorderBlue',
               'placeholder': 'رمز جدید'}), required=False, validators=[validate_password, ])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'card_number', 'shaba_number', 'current_password', 'password')

    def clean_current_password(self, value):
        user = authenticate(username=self.instance.phone_number, password=value)
        if not user:
            raise ValidationError('رمز عبور فعلی شما اشتباه است!')
        return value

    def clean_password(self, value):
        if value:
            return value
        return self.instance.password

    def clean_phone_number(self, value):
        user = User.objects.filter(phone_number=value).exclude(id=self.instance.id)
        if user.exists():
            raise ValidationError('کاربری با این شماره از قبل وجود دارد!')
        return value

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['receiver_name', 'phone_number', 'city', 'address', 'postalcode', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }
