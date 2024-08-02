from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import User, OTP, Address
from accounts.forms import UserCreationForm, UserChangeForm


admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("phone_number", "full_name", "is_superuser", "created")
    list_filter = ("is_superuser", )
    searching_fields = ("phone_number", "first_name", "last_name")
    ordering = ("-created", )
    fieldsets = (
        (
            None,
            {
                "fields": ("phone_number",
                           "first_name",
                           "last_name",
                           "password",
                           "card_number",
                           "shaba_number",
                           "last_login"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password",
                    "is_superuser",
                ),
            },
        ),
    )

    def full_name(self, obj):
        return obj.get_full_name
    full_name.short_description = 'نام و نام خانوادگی'


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created")
    list_filter = ("created", )
    search_fields = ("phone_number", "code")


@admin.register(Address)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("get_user", "receiver_name", "phone_number", "state", "city")
    list_filter = ("state", "city")
    search_fields = ("phone_number", "city")

    def get_user(self, obj):
        return obj.user
    get_user.short_description = 'کاربر'
