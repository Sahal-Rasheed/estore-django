from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import RegistrationForm
from twilio.rest import Client
from django.conf import settings

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
            login(request, user)
            # messages.success(request, f' welcome {username} !!')
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

