
#from email import message
# import email

from django.shortcuts import redirect, render
import requests
from store.models import Cart,CartItem
from .models import Account
from .forms import registrationform, VerifyForm
from .otp import send,check
from django.contrib import messages,auth
from django.contrib.auth import authenticate, logout
from store.views import _cart_id
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
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                   
                   
                   #get the product variations by the cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                     
                    #get the items from the user access his product  variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation =  item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id(index)
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
    
            auth.login(request, user)
            # messages.success(request, 'you are logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)  
            except:
                return redirect('home')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You Were Logged Out')
    return redirect('login')


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
