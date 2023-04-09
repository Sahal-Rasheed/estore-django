from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_home, name='cart_home'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart_plus/<int:product_id>/', cart_plus, name='cart_plus'),
    path('cart_minus/<int:product_id>/', cart_minus, name='cart_minus'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('checkout/', checkout, name='checkout'),
    path('coupon_apply/', coupon_apply, name='coupon_apply'),
    path('remove_coupon/', remove_coupon, name='remove_coupon'),



]
