from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.conf import settings
import datetime
import json
import razorpay

# Email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from store.models import Product
from cart.models import CartItem,Coupon,AppliedCoupon
from .models import Order, Payment, OrderProduct
from .forms import OrderForm
# Create your views here.

def Payments(request):
    # Getting data from frontend after transaction and updating order,payment,orderproduct models with these data after the payment is success
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save() 

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id      
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # Reduce quantity of the sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Deleting the cartitem after successfull order
    CartItem.objects.filter(user=request.user).delete()

    # Deleting the coupon from session and add it to usedcoupon after successfull order
    if 'coupon' in request.session:
        try:
            coupon = request.session['coupon']
            coupon_applied = Coupon.objects.get(coupon=coupon)
            x = AppliedCoupon.objects.create(user=request.user,coupon=coupon_applied)
            x.save()
            del request.session['coupon']
        except:
            pass

    # Send confirmation mail of order received to the customer 
    email_subject = 'Estore , Thank you for your order !'
    email_body = render_to_string('order_confirmation_email.html',{
        'user'      : request.user,  
        'order'     : order,
        'cart_items': cart_items,
        'product'   : product,
    })
    to_email = request.user.email
    send_email = EmailMessage(email_subject, email_body, to=[to_email])
    send_email.send()
        
    # Send order_number , transaction_id back to frontend through json resposne
    data = {
        'order_number' : order.order_number,
        'transID'      : payment.payment_id, 
    }
    return JsonResponse(data)

def Razorpay(request):
    order_number = request.GET.get("order_id")
    payment_id = request.GET.get("transaction_id")
    print(order_number)
    print(payment_id)

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    payment = Payment(
        user = request.user,
        payment_id = payment_id,
        payment_method = 'Razorpay',
        amount_paid = order.order_total,
        status = 'COMPLETED',
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save() 

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id      
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # Reduce quantity of the sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Deleting the cartitem after successfull order
    CartItem.objects.filter(user=request.user).delete()

    # Deleting the coupon from session and add it to usedcoupon after successfull order
    if 'coupon' in request.session:
        try:
            coupon = request.session['coupon']
            coupon_applied = Coupon.objects.get(coupon=coupon)
            x = AppliedCoupon.objects.create(user=request.user,coupon=coupon_applied)
            x.save()
            del request.session['coupon']
        except:
            pass


    # Send confirmation mail of order received to the customer 
    email_subject = 'Estore , Thank you for your order !'
    email_body = render_to_string('order_confirmation_email.html',{
        'user'      : request.user,  
        'order'     : order,
        'cart_items': cart_items,
        'product'   : product,
    })
    to_email = request.user.email
    send_email = EmailMessage(email_subject, email_body, to=[to_email])
    send_email.send()

    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        order_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for x in order_products:
            subtotal += x.product_price * x.quantity

        payment = Payment.objects.get(payment_id=payment_id)

        context = {
            'order' : order,
            'order_products' : order_products,
            'payment' : payment,
            'subtotal' : subtotal,
        }

        return render(request, 'order_complete.html', context)

    except (Payment.DoesNotExist , Order.DoesNotExist):
        return redirect('store')




def PlaceOrder(request, total=0, quantity=0):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    if cart_items.count() <= 0:
        return redirect('store') 
    
    if 'coupon' in request.session:
        coupon = request.session['coupon']
        x = Coupon.objects.get(coupon=coupon)
        discount = x.discount
    else:
        discount = 0
        
    grand_total = 0
    tax = 0 
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity) 
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = (tax + total) - discount  

    ###########################################
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        "amount": (grand_total)*100,
        "currency": "USD",
        'payment_capture':1,
    })
    ###########################################
    print(payment)

    order_number = None
    if request.method == 'POST':
        selected_value = request.POST.get('exampleRadios')
        # request.session['selected_value'] = selected_value
        form = OrderForm(request.POST)
        print(form.errors)

        if form.is_valid():
            order = Order()
            order.user = user
            order.first_name = form.cleaned_data.get('first_name')
            order.last_name = form.cleaned_data.get('last_name')
            order.email = form.cleaned_data.get('email')
            order.phone = form.cleaned_data.get('phone')
            order.address_1 = form.cleaned_data.get('address_1')
            order.address_2 = form.cleaned_data.get('address_2')
            order.country = form.cleaned_data.get('country')
            order.state = form.cleaned_data.get('state')
            order.city = form.cleaned_data.get('city')
            order.order_note = form.cleaned_data.get('order_note')
            order.order_total = grand_total
            order.tax = tax
            order.ip_address = request.META.get('REMOTE_ADDR')
            order.save()
            if selected_value == 'paypal':
                order_number = str(int(datetime.datetime.now().strftime('%Y%m%d%H%H%S')))
                order.order_number  = order_number
                order.save()
            else:
                order_number = payment['id']
                order.order_number = order_number
                order.save()

            order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
            print(order.order_number)

            
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'grand_total' : grand_total,
                'tax' : tax,
                'payment' : payment,
                'selected_value' : selected_value,
            }
            return render(request, 'payment.html',context)
    else:
        return redirect('checkout')
        

def OrderComplete(request):
    order_number = request.GET.get("order_id")
    payment_id = request.GET.get("transaction_id")
    print(order_number)
    print(payment_id)

    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        order_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for x in order_products:
            subtotal += x.product_price * x.quantity

        payment = Payment.objects.get(payment_id=payment_id)

        context = {
            'order' : order,
            'order_products' : order_products,
            'payment' : payment,
            'subtotal' : subtotal,
        }

        return render(request, 'order_complete.html', context)

    except (Payment.DoesNotExist , Order.DoesNotExist):
        return redirect('store')
