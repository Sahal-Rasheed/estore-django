from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('store/', store, name='store'),
    path('store/<slug:category_slug>/', store, name='category_products'),
    path('store/<slug:category_slug>/<slug:product_slug>', product_details, name='product_details'),
    path('search/', search, name="search"),
    path('pricefilter/', priceFilter, name="pricefilter"),
    path('product_review/<int:product_id>', product_review, name="product_review"),

]
