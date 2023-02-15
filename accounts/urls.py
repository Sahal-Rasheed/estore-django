from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='registration'),
    path('login/', UserLogin, name='login'),
    path('logout/', UserLogout, name='logout'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('phone_verification/', PhoneVerification, name='phoneverification'),
    path('otplogin/', OtpLogin,name='otplogin'),
    path('otpenter/', OtpEnter,name='otpenter'),
    path('forgetpassword/', ForgetPassword, name='forgetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', ResetPasswordValidate, name='resetpasswordvalidate'),
    path('resetpassword/', ResetPassword, name='resetpassword'),


]