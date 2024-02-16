import json

from django.contrib.auth import authenticate, login, get_user_model
# Create your views here.
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


class CustomLoginView(DjangoLoginView):
    template_name = 'login.html'
    next_page = '/posts'


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username, password = data['username'], data['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            return JsonResponse({'message': 'Wrong credentials, user was not logged in'}, status=401)
        login(request, user)
        return JsonResponse({'message': 'User was logged in successfully'})


@method_decorator(csrf_exempt, name="dispatch")
class SignupView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            username, password, email, phone = data['username'], data['password'], data['email'], data['phone']
        except KeyError as e:
            return JsonResponse({'message': 'Necessary fields for register were not sent'}, status=400)

        # First way to check duplicate username
        # try:
        #     user = User.objects.get(username=username)
        #     return JsonResponse({'message': 'There is already an existing user with this username'}, status=400)
        # except User.DoesNotExist:
        #     pass

        # Second way to check duplicate username
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'There is already an existing user with this username'}, status=400)

        user = User.objects.create_user(username, email=email, password=password, phone=phone)

        # Optional: based on whether we want to login user in signup api
        # login(request, user)
        return JsonResponse({'message': 'User was registered successfully'})
