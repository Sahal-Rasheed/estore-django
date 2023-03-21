from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from orders.models import Payment, OrderProduct
from store.models import Product,Category
from accounts.models import Account

# Create your views here.

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

