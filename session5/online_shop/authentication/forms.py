from django import forms
from django.contrib.auth.forms import UserCreationForm

from authentication.models import UserType, CustomUser


class UserCreateForm(UserCreationForm):
    phone = forms.CharField(max_length=11)
    user_type = forms.ChoiceField(choices=UserType.choices)
    fellow_document = forms.FileField(required=False, allow_empty_file=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'phone', 'user_type', 'fellow_document')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        fellow_document = cleaned_data.get('fellow_document')
        if user_type == UserType.fellow and not fellow_document:
            self.add_error('fellow_document', 'fellow document is required when user is of type fellow')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit)
        if self.cleaned_data.get('user_type') == UserType.fellow:
            user.is_active = False
            if commit:
                user.save()
        return user
