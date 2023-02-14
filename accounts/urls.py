from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='registration'),
    path('login/', UserLogin, name='login'),
    path('logout/', UserLogout, name='logout'),
    path('phone_verification/', PhoneVerification, name='phoneverification'),
    path('otplogin/', OtpLogin,name='otplogin'),
    path('otpenter/', OtpEnter,name='otpenter'),
    path('forgetpassword/', ForgetPassword, name='forgetpassword'),
    path('resetpassword/<uidb64>/<token>/', ResetPasswordValidate, name='resetpasswordvalidate'),
    path('resetpassword/', ResetPassword, name='resetpassword'),



]