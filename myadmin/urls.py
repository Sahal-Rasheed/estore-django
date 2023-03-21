from django.urls import path
from .views import *


urlpatterns = [
    path('', AdminHome, name='adminhome'),
    path('user_table/', UsersTable, name='user_table'),
    path('block_user/<int:id>', BlockUser, name='block_user'),
    path('product_table/', ProductTable, name='product_table'),




]