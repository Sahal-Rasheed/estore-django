from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='registration'),
    path('login/', UserLogin, name='login'),
    path('logout/', UserLogout, name='logout'),
    path('phone_verification/', PhoneVerification, name='phoneverification'),
    path('otplogin/',OtpLogin,name='otplogin'),
    path('otpenter/',OtpEnter,name='otpenter'),

]