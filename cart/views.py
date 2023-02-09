from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from .models import Cart,CartItem,Wishlist

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# add to cart in product detail page , it gets call when 1st time product is added to cart from pro details page
def add_to_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity = 1,
        )
        cart_item.save()
    
    return redirect('cart_home')

# add to cart itself its called only after a product is added from pro details page to cart page , it is cart + in cart page (to increase quantity)
def cart_plus(request,product_id):
    total=0
    quantity=0
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity = 1,
        )
        cart_item.save()
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) 
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'cart_htmx.html', context)
    # return redirect('cart')

# remove from cart itself its called only after a product is added from pro details page to cart page , it is cart - in cart page (to decrease quantity)
def cart_minus(request,product_id):
    total=0
    quantity=0
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()    
        else:
            cart_item.delete()
    except:
        pass
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) 
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'cart_htmx.html', context)
    
    # return redirect('cart')

#remove item from cart
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    # cart_item.save()
    return redirect('cart_home')

#this is the view for orginal cart page (basically can say cart_home_page)
def cart_home(request, cart_items=None, total=0, quantity=0):
    tax=0
    grand_total=0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) 
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'cart.html', context)

def add_to_wishlist(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    
    try:
        wished_pro = Wishlist.objects.create(product=product,cart=cart)
        # wished_pro.product.in_wishlist = True
        # wished_pro.product.save()
        wished_pro.save()
        return redirect(wishlist)
    except:
        pass
    if 'add_to_wishlist' in  request.path:
        wished_pro = Wishlist.objects.get(product=product,cart=cart)
        if wished_pro in Wishlist.objects.get(cart=cart):
            wished_pro.delete()
            return redirect('')
    
      

def wishlist(request):
    wishlist=None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        wishlist = Wishlist.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        pass
    
    return render(request, 'wishlist.html', {'wishlist':wishlist})

def remove_from_wishlist(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(product=product,cart=cart)
    wishlist.delete()
    # wishlist.product.in_wishlist = False
    # wishlist.product.save()
        

    # cart_item.save()
    return redirect('wishlist')