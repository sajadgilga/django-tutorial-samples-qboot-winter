from django.urls import path

from authentication.views import LoginView, SignupView, CustomLoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_user'),
    path('login/form/', CustomLoginView.as_view(), name='login_user_form'),
    path('signup/', SignupView.as_view(), name='signup_user'),
]
