
from . models import Category, SubCategory, Cart, CartItem
from . views import _cart_id



def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
def subcat_links(request):
    link = SubCategory.objects.all()
    return dict(link=link)
def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
            