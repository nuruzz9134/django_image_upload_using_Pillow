from django.urls import path
from authentication.views import *

urlpatterns = [
    path('superuser/',Creatsuperuserview.as_view()),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('verify_otp/',VerifyOTP.as_view()),
    path('password_change/',PasswordChangeView.as_view()),
]