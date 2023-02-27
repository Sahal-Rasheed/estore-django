from django.urls import path
from .views import *

urlpatterns = [
    path('place_order/', PlaceOrder, name='place_order'),
    path('payment/', Payments, name='payment'),
    path('order_complete/', OrderComplete, name='order_complete'),


]