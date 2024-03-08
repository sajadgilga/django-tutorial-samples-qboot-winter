import random

from django.conf.global_settings import EMAIL_HOST
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from authentication.models import OTPCode, ImageUpload

User = get_user_model()


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def _generate_otp(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def validate(self, attrs):
        email = attrs['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError('User does not exist')

        code = self._generate_otp()

        OTPCode.objects.create(code=code, email=email)

        # send email
        send_mail(
            'Sample Login OTP',
            f'Dear user,\nyour otp to login is {code}',
            from_email=EMAIL_HOST,
            recipient_list=[email]
        )
        return attrs


class CustomObtainTokenSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop('password')
        self.fields['code'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            'email': attrs[self.username_field],
            'code': attrs['code'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        if not self.user:
            raise ValidationError('User does not exist')

        data = {}
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'original_image']
