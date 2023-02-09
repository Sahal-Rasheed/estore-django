def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                phone_number=form.cleaned_data['phone_number'],
            )
            request.session['phone_number'] = form.cleaned_data['phone_number']

            # Replace the ACCOUNT_SID, AUTH_TOKEN, and PHONE_NUMBER_VERIFY_SID with your own
            ACCOUNT_SID = 'your_account_sid'
            AUTH_TOKEN = 'your_auth_token'
            PHONE_NUMBER_VERIFY_SID = 'your_phone_number_verify_sid'
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            verification = client.verify \
                .services(PHONE_NUMBER_VERIFY_SID) \
                .verifications \
                .create(to=form.cleaned_data['phone_number'], channel='sms')
            
            return redirect('verify_phone_number')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def verify_phone_number(request):
    if request.method == 'POST':
        # Replace the ACCOUNT_SID, AUTH_TOKEN, and PHONE_NUMBER_VERIFY_SID with your own
        ACCOUNT_SID = 'your_account_sid'
        AUTH_TOKEN = 'your_auth_token'
        PHONE_NUMBER_VERIFY_SID = 'your_phone_number_verify_sid'
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        phone_number = request.session.get('phone_number', '')
        verification_check = client.verify \
            .services(PHONE_NUMBER_VERIFY_SID) \
            .verification_checks \
            .create(to=phone_number, code=request.POST.get('otp'))
        
        if verification_check.status == 'approved':