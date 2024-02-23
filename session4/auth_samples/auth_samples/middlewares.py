from datetime import datetime

import jwt
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from auth_samples.settings import TOKEN_DATE_FORMAT
from authentication.models import Token

User = get_user_model()


class LoggingMiddleware:
    def __init__(self, get_response):
        print("Middleware setup")
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print(f"Request {request.path} called")
        response = self.get_response(request, *args, **kwargs)
        print(f"Response retrieved successfully {response.status_code}")
        return response


def FunctionalLoggingMiddleware(get_response):
    print("Function middleware setup")

    def middleware(request, *args, **kwargs):
        print(f"Request {request.path} called")
        response = get_response(request, *args, **kwargs)
        print(f"Response retrieved successfully {response.status_code}")
        return response

    return middleware


class CustomAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_anonymous:
            return
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], verify=True)
            Token.objects.get(token=token)
        except (jwt.DecodeError, jwt.ExpiredSignatureError, Token.DoesNotExist):
            return HttpResponse('Token not valid', status=401)

        now = datetime.now()
        if datetime.strptime(payload['expire_time'], TOKEN_DATE_FORMAT) < now:
            return HttpResponse('Token expired', status=401)

        user_id = payload.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponse('User does not exist with this id', status=401)
        request.user = user
