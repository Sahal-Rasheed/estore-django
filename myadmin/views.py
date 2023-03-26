from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib import messages
import datetime
import csv
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate,login,logout
from orders.models import Payment, OrderProduct, Order
from store.models import Product,Category
from accounts.models import Account
from .models import Banner

# Create your views here.
def AdminLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_superadmin:
                login(request,user)
                return redirect('adminhome')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('admin_login')
        else:
            messages.error(request,"Invalid Credentials")
    
    return render(request, 'myadmin/admin_login.html')

def AdminLogout(request):
    logout(request)
    return redirect('admin_login')

def AdminHome(request):
    paypal_total = 0
    razorpay_total = 0
    total_earning = 0
    sold_products = 0
    paypal = Payment.objects.filter(payment_method='Paypal')
    for i in paypal:
        paypal_total += float(i.amount_paid)

    razorpay = Payment.objects.filter(payment_method='Razorpay')
    for i in razorpay:
        razorpay_total += float(i.amount_paid)

    total = Payment.objects.all()
    for i in total:
        total_earning += float(i.amount_paid)

    sold_products = OrderProduct.objects.all().count()

    context = {
        'paypal_total' : paypal_total,
        'razorpay_total' : razorpay_total,
        'total_earning' : total_earning,
        'sales' : sold_products,
    }
    
    return render(request, 'myadmin/admin_home.html', context)

def UsersTable(request):
    users = Account.objects.all()
    context = {
        'users' : users,
    }

    return render(request, 'myadmin/users_table.html', context)

def BlockUser(request,id):
    user = Account.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect(UsersTable)

def ProductTable(request):
    products = Product.objects.all().order_by('created_date')
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)  # returns the desired page object
    context = {
        'products' : page_products,
    }

    return render(request, 'myadmin/product_table.html', context)

def EditProduct(request,id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        if product_name == "" or description == "" or price == "" or stock == "" or image == "":
            messages.error(request, "All Fields Are Required")
        else:
            product_obj = Product.objects.get(id=id)
            product_obj.product_name = product_name
            product_obj.description = description
            product_obj.price = price
            product_obj.stock = stock
            product_obj.slug = slugify(product_name)
            if image:
                product_obj.product_image = image 
            else:
                pass 
            product_obj.save()
            return redirect('product_table')

    context = {
        'product' : product,
        'categories' : categories,
    }
    return render(request, 'myadmin/edit_product.html', context)

def AddProduct(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if product_name == "" or description == "" or price == "" or stock == "" or image == "" or category == "":
            messages.error(request, "All Fields Are Required")
        else:
            product = Product(
                product_name = product_name, description = description, price = price, stock = stock, product_image = image
            )
            product.category = Category.objects.get(id=category)
            product.slug = slugify(product_name)
            product.save()
            return redirect('product_table')

    context = {
        'categories' : categories,
    }

    return render(request, 'myadmin/add_product.html', context)

def DeleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product_table')

def CategoryTable(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request, 'myadmin/category_table.html', context)

def EditCategory(request,id):
    category = Category.objects.get(id=id)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if category_name == "" or description == "" or image == "":
            messages.error(request, "All Fields Are Required")
        else:
            category_obj = Category.objects.get(id=id)
            category_obj.category_name = category_name
            category_obj.description = description
            category_obj.slug = slugify(category_name)
            if image:
                category_obj.category_image = image 
            else:
                pass 
            category_obj.save()
            return redirect('category_table')

    context = {
        'category' : category,
    }
    return render(request, 'myadmin/edit_category.html', context)

def AddCategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if category_name == "" or description == "" or image == "":
            messages.error(request, "All Fields Are Required")
        else:
            category = Category(
                category_name = category_name, description = description, category_image = image
            )
            category.slug = slugify(category_name)
            category.save()
            return redirect('category_table')

    return render(request, 'myadmin/add_category.html')

def DeleteCategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('category_table')

def OrderTable(request):
    orders = Order.objects.filter(is_ordered=True).order_by('created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_orders = paginator.get_page(page_number)  # returns the desired page object
    context = {
        'orders' : page_orders
    }

    return render(request, 'myadmin/order_table.html', context)

def ViewOrder(request, id):
    order = Order.objects.get(id=id)
    order_products = OrderProduct.objects.filter(order=order)
    context = {
        'order_products' : order_products,
    }

    return render(request, 'myadmin/view_order.html', context)

def OrderStatus(request, id):
    url = request.META.get('HTTP_REFERER')
    order_product = OrderProduct.objects.get(id=id)
    if request.method == "POST":
        status = request.POST.get('status')
        order_product.status = status
        order_product.save()

    return redirect(url)

def BannerTable(request):
    banners = Banner.objects.all()
    return render(request, 'myadmin/banner_table.html', {'banners':banners})

def AddBanner(request):
    if request.method == 'POST':
        image = request.FILES.get('banner')
        banner = Banner(banner=image)
        banner.save()
        return redirect('banner_table')

    return render(request, 'myadmin/add_banner.html')


def EditBanner(request, id):
    url = request.META.get('HTTP_REFERER')
    banner = Banner.objects.get(id=id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'Live':
            banner.is_live = True
        else:
            banner.is_live = False
        banner.save()
    return redirect(url)

def DeleteBanner(request, id):
    banner = Banner.objects.get(id=id)
    banner.delete()
    return redirect('banner_table')

def SalesTable(request):
    orders = Order.objects.filter(is_ordered=True).order_by('id')
    # paginator = Paginator(orders, 10)
    # page_number = request.GET.get('page')
    # page_orders = paginator.get_page(page_number) 
    context = {
        'orders' : orders
    }

    return render(request, 'myadmin/sales_table.html', context)

def SalesDate(request):
    if request.method == 'POST':
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')

        f_date = from_date.split('-')
        t_date = to_date.split('-')

        start_date = [int(x) for x in f_date]
        end_date = [int(x) for x in t_date]

        orders = Order.objects.filter(is_ordered=True, created_at__gte = datetime.date(start_date[0],start_date[1],start_date[2]),created_at__lte = datetime.date(end_date[0],end_date[1],end_date[2]) )
        
    context = {
        'orders' : orders
    }

    return render(request, 'myadmin/sales_table.html', context )



def SalesMonthly(request, date):
    f =date
    from_date = [2023, f, 1]
    to_date = [2023, f, 28]

    orders = Order.objects.filter(is_ordered=True, created_at__gte = datetime.date(from_date[0],from_date[1],from_date[2]),created_at__lte = datetime.date(to_date[0],to_date[1],to_date[2]) )
      
    context = {
        'orders' : orders
    }

    return render(request, 'myadmin/sales_table.html', context)

def SalesYearly(request, date):
    f =date
    from_date = [f, 1, 1]
    to_date = [f, 12, 31]

    orders = Order.objects.filter(is_ordered=True, created_at__gte = datetime.date(from_date[0],from_date[1],from_date[2]),created_at__lte = datetime.date(to_date[0],to_date[1],to_date[2]) )
      
    context = {
        'orders' : orders
    }

    return render(request, 'myadmin/sales_table.html', context)


# Simple CSV Write Operation
def SalesCSV(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['order_id', 'customer', 'order_total', 'payment_mode', 'date'])
    orders = Order.objects.filter(is_ordered=True)
    for order in orders:
        writer.writerow([order.order_number, order.first_name, order.order_total, order.payment.payment_method, order.created_at])
    return response