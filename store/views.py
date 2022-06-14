from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem, Category, Product, SubCategory, Variation
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    category = Category.objects.all().filter().order_by('-id')[0:6]
    context={
         'category': category,
    }
    return render(request, 'home.html',context)


def category(request, category_slug=None, subcategory_slug=None):
    categories = None
    products = None
    SubCategorys = None
    subcat=SubCategory.objects.filter(slug=category_slug)
    
    if category_slug != None: 
        categories =get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        if subcategory_slug != None:
            SubCategorys =get_object_or_404(SubCategory, slug=subcategory_slug)
            products = Product.objects.filter(SubCategory=SubCategorys, is_available=True)
            paginator = Paginator(products,6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            
    else:
    
        products = Product.objects.all()
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'subcat': subcat,
        'product': product_count,
        'categories': categories,
    }
    return render(request, 'category.html', context) 





def productdetail(request, category_slug, subcategory_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, SubCategory__slug=subcategory_slug, slug=product_slug)
        related_product = Product.objects.filter(SubCategory__slug=subcategory_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'related_product': related_product,  
    }
    return render(request, 'product-detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-id').filter(Q(description__icontains= keyword) | Q(product_name__icontains= keyword) | Q(category__category_name__icontains= keyword))
            product_count = products.count()
        else:
            return redirect('category')
    context = {
       'products': products,   
       'product': product_count,
    }        
    return render(request,'category.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    
    product = Product.objects.get(id=product_id) # get the product   
    product_variation = []
    if request.method == 'POST':
        
        for item in request.POST:
            print(item)
            key = item
            value = request.POST[key]
            

            try:
                print("try One")
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                print(variation)
                product_variation.append(variation)
                print("toooo")
                print(product_variation)
                print("gioooo")
                # product_variation.reverse()
                # print(product_variation)
            except:
                pass
            
      
    try:
        print('try Two')
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id =_cart_id(request)
        )
    cart.save() 
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation =  item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        if product_variation in ex_var_list:
            #increase the current item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            #create  a new cart item
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
     
    else: 
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else: 
            cart_item.delete()
    except:
        pass
            
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    

def cart(request, total=0, quantity=0, cart_items=None):
    tax=0
    grand_total=0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items =CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
        tax = (2 * total)/100
        grand_total = total + tax
        print(quantity)
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total, 
    }
    return render(request, 'cart.html', context)
 