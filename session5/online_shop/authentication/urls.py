from django.urls import path

from authentication.views import SignupView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('signup/', SignupView.as_view(), name='signup_view'),
]
