from django import forms
from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authentication.models import CustomUser


class CustomUserAddForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone"]

    def clean_password_repeat(self):
        password = self.cleaned_data.get('password1')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password and password_repeat and password_repeat != password:
            raise ValidationError("Input passwords do not match!")
        return password_repeat

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    add_form = CustomUserAddForm
    add_fieldsets = (
        (
            "Base Info",
            {
                "classes": ("wide",),
                "fields": ("username", "email", "phone"),
            },
        ),
        (
            "Password",
            {
                "fields": ("password1", "password_repeat")
            }
        )
    )
    list_display = ("username", "email", "phone", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
