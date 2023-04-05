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
    path('my_orders/', MyOrders, name='myorders'),
    path('edit_profile/', EditProfile, name='editprofile'),
    path('order_detail/<str:order_number>', OrderDetails, name='order_details'),
    path('order_tracking/<int:orderpro_id>', OrderTrack, name='order_tracking'),
    path('change_password/', ChangePassword, name='change_password'),




]