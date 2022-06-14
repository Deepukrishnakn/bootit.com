
#from email import message
# import email
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import Account
from .forms import registrationform, VerifyForm
from .otp import send,check
from django.contrib import messages,auth
from django.contrib.auth import authenticate

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

 
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = registrationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            request.session['phone_number'] = phone_number
            send(form.cleaned_data.get('phone_number'))
            return redirect('otp')
    else:
        form = registrationform()
    context={
        'form':form,
            }
    return render(request, 'accounts/register.html',context)
def otp(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_number = request.session['phone_number']
            if check(phone_number, code):
                user = Account.objects.get(phone_number=phone_number)
                user.is_active= True
                user.save()
                return redirect('login')
    else:
        form = VerifyForm()
    return render(request, 'accounts/otp.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password') 
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'you are logged in')
            return redirect('home')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    pass


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            
            
            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'pleace activate your account'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'password reset email has been sent to your email')
            return redirect('login')
        else:
            messages.error(request, 'Account doses not exist')
    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'pleace reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successful')
            return redirect('login')
        
        else:
            messages.error(request, 'password do not match!')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')
        