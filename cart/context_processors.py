from .views import _cart_id
from .models import Cart,CartItem,Wishlist

def cart_counter(request):
    cart_counter=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items=CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_counter += cart_item.quantity
        except Cart.DoesNotExist:
            cart_counter=0
    return dict(cart_counter=cart_counter)

def wishlist_counter(request):
    wishlist_counter=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            wishlist = Wishlist.objects.all().filter(cart=cart[:1])
            
            for wish in wishlist:
                if wish.product:
                    wishlist_counter += 1
                else:
                    pass

        except Cart.DoesNotExist:
            wishlist_counter=0
    return dict(wishlist_counter=wishlist_counter)


def in_wishlist(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            wishlists = Wishlist.objects.filter(cart=cart)
            wishlist = []
            for item in wishlists:
                wishlist.append(item.product.product_name)
        except Cart.DoesNotExist:
            wishlist = None   
    return {'wishlist':wishlist}


