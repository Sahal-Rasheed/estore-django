from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account,UserProfile
from .forms import RegistrationForm,UserForm,UserProfileForm
from twilio.rest import Client
from django.conf import settings

# Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart.views import _cart_id
from cart.models import CartItem,Cart,Wishlist
from orders.models import Order,OrderProduct,OrderTracking

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            # password2 = form.cleaned_data.get('confirm_password')
            username = email.split('@')[0]    

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password, username=username)
            user.save()
            request.session['phone_number'] = phone_number
            phone_no = '+91' + phone_number

            messages.success(request, 'Activate your account now!')

            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid,auth_token)
            verification = client.verify \
                        .services(settings.SERVICES) \
                        .verifications \
                        .create(to= phone_no, channel='sms')

            return redirect('phoneverification')             
    else:
        form = RegistrationForm()
        
    context = {
        'form':form
    }
    return render(request, 'registration.html', context)

def UserLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                guest_cart = CartItem.objects.filter(cart=cart)
                user_cart = CartItem.objects.filter(user=user)
                
                for gitem in guest_cart:
                    for uitem in user_cart:
                        if gitem.product == uitem.product:
                            uitem.quantity += gitem.quantity
                            gitem.delete()
                            uitem.save()
                      
                cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    for item in cart_items:
                        item.user = user
                        item.save()
            except:
                pass

            login(request, user)
            # messages.success(request, f' welcome {username} !!')
            next_url = request.META.get('HTTP_REFERER')
            print(next_url)
            if '/cart/checkout/' in next_url :
                return redirect('checkout')
            else:
                return redirect('home')
        else:
            messages.error(request,'Invalid Credentials!')
            return redirect('login')

    return render(request, 'login.html')

def PhoneVerification(request):
    phone_number = request.session.get('phone_number')

    if 'phone_number' in request.session:
        if request.method == 'POST':
            phone_number = request.session.get('phone_number')
            phone_no = '+91' + phone_number
            otp_input      = request.POST.get('otp')
            
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid,auth_token)
            verification_check = client.verify \
                                .services(settings.SERVICES) \
                                .verification_checks \
                                .create(to= phone_no, code=otp_input)

            if verification_check.status == "approved":
                    user = Account.objects.filter(phone_number=phone_number).last()
                    user.is_active = True
                    user.save()
                    request.session.flush()
                    return redirect('login')    
            else:
                    messages.error(request,'Invalid OTP')
                    return render(request,'phone_verification.html')
    else:
        return redirect('registration')
        
    context = {
        'userph':phone_number
    }
        
    return render(request, 'phone_verification.html', context)

def OtpLogin(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        phone_no = '+91' + phone_number
        if Account.objects.filter(phone_number=phone_number).exists():
            # user = Account.objects.get(phone_number = phone_number)
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid,auth_token)
            verification = client.verify \
                .services(settings.SERVICES) \
                .verifications \
                .create(to=phone_no ,channel='sms')
            request.session['phone_number'] = phone_number
            return redirect('otpenter') 
        else:
            messages.error(request,'There is no Account that matches with this Phone Number. Enter a Valid Phone Number!')
            return redirect("otplogin")
    return render(request, 'otplogin.html')

def OtpEnter(request):
    phone_number = request.session.get('phone_number')
    if 'phone_number' in request.session:
        if request.method == 'POST':
            phone_no = "+91" + phone_number
            otp_input   = request.POST.get('otp')

            if len(otp_input)>3:
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.AUTH_TOKEN
                client = Client(account_sid, auth_token)
            
                verification_check = client.verify \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)

                if verification_check.status == "approved":
                    user = Account.objects.get(phone_number=phone_number)
                    login(request,user)
                    del request.session['phone_number']
                    return redirect('home')
                else:
                    messages.error(request,'Invalid OTP')
                    return render(request,'otpenter.html')
            else:
                messages.error(request,'Invalid OTP')
                return redirect('otplogin')
    else:
        return redirect('otplogin')
    return render(request,'otpenter.html')

@login_required(login_url='login')
def UserLogout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            email_subject = 'Estore, Password Reset Mail'
            email_body = render_to_string('password_reset_email.html',{
                'user'   : user,
                'domain' : current_site,
                'uid'    : urlsafe_base64_encode(force_bytes(user.pk)),
                'token'  : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject, email_body, to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'This email does not matches with any account.')
            return redirect('forgetpassword')
    return render(request,'forgetpassword.html')

def ResetPasswordValidate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def ResetPassword(request):
    uid = request.session.get('uid')
    if 'uid' in request.session:
        if request.method == 'POST':
            new_pass = request.POST.get('npass')
            c_pass = request.POST.get('cpass')
            if new_pass == c_pass:
                try:
                    user = Account.objects.get(pk=uid)
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, 'Your password has been changed successfully.')
                    del request.session['uid']
                    return redirect('login')
                except Account.DoesNotExist:
                    return redirect('forgetpassword')
            else:
                messages.error(request, 'Password not matching.')
                return redirect('resetpassword')
        else:
            return render(request,'resetpassword.html')
    else:
        return redirect('forgetpassword')

@login_required(login_url='login')
def Dashboard(request):
    total_orders = 0
    net_spend = 0
    pending_orders_count = 0
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    pending_orders = OrderProduct.objects.order_by('-created_at').filter(user_id=request.user.id, ordered=True,status='Processing')
    pending_orders_count = pending_orders.count() 

    total_orders = orders.count()
    
    for order in orders:
        net_spend += order.order_total

    context = {
        'total_orders' : total_orders,
        'net_spend' : net_spend,
        'pending_orders_count' : pending_orders_count,
    }
    return render(request,'dashboard.html',context)

@login_required(login_url='login')
def MyOrders(request):
    order_products = OrderProduct.objects.order_by('-created_at').filter(user=request.user, ordered=True)
    context = {
        'order_products' : order_products,
    }

    return render(request,'my_orders.html', context)

@login_required(login_url='login')
def EditProfile(request):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        userprofile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        userform = UserForm(data=request.POST, instance=request.user)
        userprofileform = UserProfileForm(data=request.POST, instance=userprofile, files=request.FILES)
        if userform.is_valid() and userprofileform.is_valid():
            userform.save()
            userprofileform.save()
            messages.success(request, 'User profile updated successfully')
            return redirect('editprofile')
        else:
            messages.error(request, 'User profile updation failed')
            return redirect('editprofile')
    else:
        userform = UserForm(instance=request.user)
        userprofileform = UserProfileForm(instance=userprofile)
    
    context = {
        'userform'        : userform,
        'userprofileform' : userprofileform,
        'userprofile'     : userprofile
    }

    return render(request,'edit_profile.html', context)

@login_required(login_url='login')
def OrderDetails(request,order_number):
    subtotal = 0
    order_detail = OrderProduct.objects.filter(order__order_number=order_number)
    order = Order.objects.get(order_number=order_number)

    for x in order_detail:
        subtotal += x.product_price*x.quantity

    context = {
        'order' : order,
        'order_detail' : order_detail,
        'subtotal' : subtotal
    }

    return render(request,'order_detail.html', context)

@login_required(login_url='login')
def ChangePassword(request):
    if request.method == 'POST':
        current_pass = request.POST.get('current_pass')
        new_pass = request.POST.get('new_pass')
        confirm_pass = request.POST.get('confirm_pass')

        user = authenticate(email=request.user.email, password=current_pass)
        print(user)
        if user:
            if new_pass == confirm_pass:
                user.set_password(new_pass)
                user.save()
                messages.success(request,'Passsword changed successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Password Mismatch')
                return redirect('change_password')
        else:
            messages.error(request,'Old password was invalid')
            return redirect('change_password')
        
    return render(request,'change_password.html')

def OrderTrack(request, orderpro_id):
    order_tracking = None
    try:
        order_tracking = OrderTracking.objects.get(order_id=orderpro_id)
    except:
        OrderTracking.DoesNotExist

    order_pro = OrderProduct.objects.get(id=orderpro_id)
    order_processing = order_pro.status
    date = order_pro.created_at
    context = {
        'order_pro' : order_pro,
        'order_tracking' : order_tracking,
        'order_processing' : order_processing,
        'date' : date,
    }

    return render(request,'order_tracking.html', context)
    



