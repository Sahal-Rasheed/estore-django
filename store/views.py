from django.shortcuts import render,get_object_or_404
from store.models import Category,Product
from cart.models import CartItem,Wishlist,Cart
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from cart.views import _cart_id

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products':products,
    }
    return render(request,'home.html',context)

def store(request,category_slug=None):
    products=None
    category=None
      
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page_products = paginator.get_page(page_number)  # returns the desired page object
        count = products.count()
   
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_products = paginator.get_page(page_number)  # returns the desired page object
        count = products.count()

    # except PageNotAnInteger:
    #     # if page_number is not an integer then assign the first page
    #     page_ob = paginator.page(1)
    # except EmptyPage:
    #     # if page is empty then return last page
    #     page_obj = paginator.page(1)

    context = {
        'products': page_products, 
        'count':count,   
    }
   
    return render(request,'store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug ,is_available=True)
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(user=request.user, product=single_product).exists()
        else: 
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
            
        wishlist = Wishlist.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'wishlist':wishlist
    }
    return render(request,'product_detail.html',context)

def search(request):
    
    query = request.GET['search'] # we are storing the string searched by the user in a query variable
    products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=query) | Q(description__icontains=query))
    count = products.count()
    
    context = {
        'products': products, 
        'count':count,
    }
   
    return render(request,'store.html',context)

def priceFilter(request):
    products=None
    count=0
    if request.method != 'GET':
        min = request.POST['min'] # we are storing the min value from dropdown in min variable
        max = request.POST['max'] # we are storing the max value from dropdown in max variable
        products = Product.objects.filter(price__range=(min, max)) # range filter to sort pro price b/w min and max
        count = products.count()
    
    context = {
        'products': products, 
        'count':count,
    }
    
    return render(request,'store.html',context)
