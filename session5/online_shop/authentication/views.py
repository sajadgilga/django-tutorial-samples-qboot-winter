from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authentication.forms import UserCreateForm


class LoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('product_list_view')


class SignupView(CreateView):
    form_class = UserCreateForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login_view')
