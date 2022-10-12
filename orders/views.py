import datetime
from genericpath import exists
import razorpay
from django.contrib.auth.decorators import login_required
from store.models import Discount_coupon
from .models import Address
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Order,Payment,OrderProduct
from store.models import CartItem,Product
# email verification
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.
@login_required(login_url = 'login')
def place_order(request,total=0, quantity=0):
    current_user = request.user

    # if the cart count is less than or equal to 0 , then redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')

    grand_total_without = 0
    grand_total = 0
    tax = 0
    dis=0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total)/100
    grand_total_without = total + tax 
    print(grand_total_without)
    try:
        data = Discount_coupon.objects.get(user=request.user)
        dis=data.discount_applied      
        print(grand_total_without)        
        grand_total = grand_total_without - float(dis)
        print(dis)
        print(grand_total)
    except:
        grand_total = grand_total_without
    
    if request.method == 'POST':
        if 'address' in request.POST:
            address_id = request.POST['address']
            address = Address.objects.get(id=address_id)
          
            # Store all Billing information in Order Table
            data = Order()   # getting instance
            data.address = address
            data.user = current_user
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            request.session['order_number']=order_number

            data.order_number = order_number
            data.save()

            context={
                'tax': tax,
                'total': total,
                'cart_items': cart_items,
                'grand_total': grand_total,
                'address': address,
                'dis': dis,
            }

            return render (request,'orders/payment.html', context)
        else:
            messages.error(request,'Please Enter a Address to Continue')
            return redirect('checkout')   
    else: 
        return redirect('checkout')                 

@login_required(login_url = 'login')
def payment(request):

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    grand_total = 0
    total= 0
    tax = 0
    grand_total_without = 0
    quantity = 0
    dis=0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
   
    tax = (2 * total)/100
    grand_total_without = (total + tax)
    data = Discount_coupon.objects.filter(user=request.user).exists()
    if data:
        data = Discount_coupon.objects.get(user=request.user)
        dis=data.discount_applied 
        print(dis)     
        print(grand_total_without)        
        grand_total = (grand_total_without - float(dis))*100
        print(dis)
        print(grand_total)
        data = Discount_coupon.objects.get(user=request.user)
        data.delete()
        
    else:
        grand_total = grand_total_without*100
    paisa = grand_total/100
   

#create razor pay client

    Client =razorpay.Client(auth=('rzp_test_FqfpAM5lIo4SFl','7ZAUh0Cwtpqz2N7MIyJ5IW1T'))
    #create order

    response_payment=Client.order.create(dict( amount=grand_total,currency='INR'))

    order_id = response_payment['id']
    order_status = response_payment['status']
    total += (cart_item.product.price * cart_item.quantity)
    if order_status == 'created':
        pay = Payment()
        pay.user = current_user
        pay.account_paid = grand_total
        pay.order_id = order_id
        pay.save()

    context= {
        'payment':response_payment,
        'grand_total':paisa,
        'tax':tax,
        'total':total,
        'dis': dis,
    }    
    return render(request,'orders/razor_payments.html',context)


@login_required(login_url = 'login')   
def payment_status(request):
    response = request.POST
    print(response)
    params_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    #client instance

    client = razorpay.Client(auth=('rzp_test_FqfpAM5lIo4SFl','7ZAUh0Cwtpqz2N7MIyJ5IW1T'))
    try:
        status =client.utility.verify_payment_signature(params_dict)
        payment=Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id=response['razorpay_payment_id'] 
        payment.paid=True 
        payment.save() 
        
        print(payment)
        

        order_number=request.session['order_number'] 
        print(order_number) 
        order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number) 
        print(order)
        print(order.order_total)
        order.payment=payment  
        order.status='Ordered' 
        order.is_ordered = True
        order.save()
        print("jijijij")
        
    #  # Move the cart item into order product table
        cart_items = CartItem.objects.filter(user=request.user)
        print(cart_items)
        print('hello')

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            print('1111')
            orderproduct.payment = payment
            print('2222')
            orderproduct.user_id =request.user.id
            print('333')
            orderproduct.product_id = item.product_id
            print('444')
            orderproduct.quantity = item.quantity
            print('55')
            orderproduct.product_price= item.product.price
            print('777')
            orderproduct.ordered = True
            print('444555232')
            orderproduct.save()
            print('617117')

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()


        #Reduced the quantity

            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()
          
       # clear cart
        CartItem.objects.filter(user=request.user).delete()

       #Send Order recieved email to customer
    
        
        mail_subject = 'Thankyou for ordering with Us'
        message = render_to_string('orders/order_recieved_email.html', {
                'user': request.user,
                'order':order,
            
            })
        to_email =request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()      
        return render(request,'orders/payment_status.html',{'status':True})
    except: 
        print("except")  
        return render(request,'orders/payment_status.html',{'status':False})
    
    
def cashon(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    grand_total = 0
    total= 0
    tax = 0
    grand_total_without = 0
    quantity = 0
    dis=0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
   
    tax = (2 * total)/100
    grand_total_without = (total + tax)
    data = Discount_coupon.objects.filter(user=request.user).exists()
    if data:
        data = Discount_coupon.objects.get(user=request.user)
        dis=data.discount_applied 
        print(dis)     
        # print(grand_total_without)        
        grand_total = (grand_total_without - float(dis))
        print(dis)
        # print(grand_total)
        data = Discount_coupon.objects.get(user=request.user)
        data.delete()
        
    else:
        grand_total = grand_total_without
        pay = Payment()
        pay.user = current_user
        pay.account_paid = grand_total
       
        pay.save()
    return render(request,'orders/cashon.html',{'grand_total':grand_total})
        
def cod_verify(request):
    print('fffff')
  
    order_number=request.session['order_number'] 
    print(order_number) 
    order=Order.objects.get(user=request.user,order_number=order_number) 
    print(order)
    print(order.order_total) 
    order.status='Ordered'  
    order.is_ordered = True
    order.save()
    
#  # Move the cart item into order product table
    cart_items = CartItem.objects.filter(user=request.user)
    print(cart_items)
    print('hello')

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id =request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price= item.product.price
        orderproduct.ordered = True
        orderproduct.save()
    print('rrrrrrr')
    cart_item = CartItem.objects.get(id=item.id)
    product_variation = cart_item.variations.all()
    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
    orderproduct.variations.set(product_variation)
    orderproduct.save()

    product = Product.objects.get(id=item.product_id)
    product.stock -= item.quantity
    product.save()
    
# clear cart
    CartItem.objects.filter(user=request.user).delete()

#Send Order recieved email to customer

    
    mail_subject = 'Thankyou for ordering with Us'
    message = render_to_string('orders/order_recieved_email.html', {
            'user': request.user,
            'order':order,
        
        })
    to_email =request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()      
    messages.success(request, 'your Order Placed successfuly')
    return redirect('home')
