from django.urls import path
from .views import *


urlpatterns = [
    path('', AdminHome, name='adminhome'),
    path('login/', AdminLogin, name='admin_login'),
    path('logout/', AdminLogout, name='admin_logout'),
    path('user_table/', UsersTable, name='user_table'),
    path('block_user/<int:id>', BlockUser, name='block_user'),
    path('product_table/', ProductTable, name='product_table'),
    path('product_table/edit_product/<int:id>', EditProduct, name='edit_product'),
    path('product_table/add_product/', AddProduct, name='add_product'),
    path('product_table/delete_product/<int:id>', DeleteProduct, name='delete_product'),
    path('category_table/', CategoryTable, name='category_table'),
    path('category_table/edit_category/<int:id>', EditCategory, name='edit_category'),
    path('category_table/add_category/', AddCategory, name='add_category'),
    path('category_table/delete_category/<int:id>', DeleteCategory, name='delete_category'),
    path('order_table/', OrderTable, name='order_table'),
    path('order_table/view_order/<int:id>', ViewOrder, name='view_order'),
    path('order_table/order_status/<int:id>', OrderStatus, name='order_status'),
    path('coupon_table/', CouponTable, name='coupon_table'),
    path('coupon_table/add_coupon/', AddCoupon, name='add_coupon'),
    path('coupon_status/<int:id>', CouponStatus, name='coupon_status'),
    path('coupon_table/delete_coupon/<int:id>', DeleteCoupon, name='delete_coupon'),
    path('banner_table/', BannerTable, name='banner_table'),
    path('banner_table/add_banner', AddBanner, name='add_banner'),
    path('banner_table/edit_banner/<int:id>', EditBanner, name='edit_banner'),
    path('banner_table/delete_banner/<int:id>', DeleteBanner, name='delete_banner'),
    path('sales_table/', SalesTable, name='sales_table'),
    path('sales_table/sales_date/', SalesDate, name='sales_date'),
    path('sales_table/sales_monthly/<int:date>', SalesMonthly, name='sales_monthly'),
    path('sales_table/sales_yearly/<int:date>', SalesYearly, name='sales_yearly'),
    path('sales_table/sales_csv/', SalesCSV, name='sales_csv'),
    path('sales_table/sales_xls/', SalesXLS, name='sales_xls'),























]