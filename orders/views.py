import datetime
from .models import Address
from pyexpat.errors import messages

from django.shortcuts import redirect, render
from orders.models import Order
from store.models import CartItem

# Create your views here.
def payment(request):
    return render(request, 'orders/payment.html')

def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    # if the cart cont is or equal to 0 then redirect back to shop
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        if 'address' in  request.POST:
            address_id=request.POST['address']
            address=Address.objects.get(id=address_id)
            data = Order()
            data.user=request.user
            data.address=address
            data.order_totel = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            request.session['oder_number']=order_number
            data.order_number = order_number
            data.save()
            
            context={
                'tax':tax,
                'total':total,
                'cart_item':cart_item,
                'grand_total':grand_total,
                'address':address,
            }
            print(address)
            return render(request, 'orders/payment.html', context)
        else:
            messages.error(request, 'please enter address for continue!!!')
            return redirect('checkout')
    else:
        return redirect('checkout')