import re
import django
from orders.models import OrderProduct
from django.db.models import Max,Min
from .forms import ReviewForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from orders.models import Address
from orders.forms import AddressForm
from .models import Cart, CartItem, Category, Product, ReviewRating, SubCategory, Variation,Discount, Wishlist,Discount_coupon,ReviewRating,filter_price
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    category = Category.objects.all().filter().order_by('-id')[0:6]
    newproduct = Product.objects.all().filter().order_by('-id')[0:6]
    context={
         'category': category,
          'newproduct': newproduct,
    }
    return render(request, 'home.html',context)

# def newproduct(request):
#     newproduct = Product.objects.all().filter().order_by('-id')[0:6]
#     context={
#          'newproduct': newproduct,
#     }
#     return render(request, 'home.html',context)


def category(request, category_slug=None, subcategory_slug=None):
    categories = None
    products = None
    SubCategorys = None
    sort_id=0
    subcat=SubCategory.objects.filter(slug=category_slug)
    
    if category_slug != None: 
        categories =get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        if 'sorting' in request.POST:
            if request.method=='POST':
                sort_id=request.POST['sorting']
                print(sort_id)
                if sort_id=='low':
                    products=Product.objects.filter(category=categories).order_by('price')
                    count=products.count()
                    paginetor = Paginator(products,6)
                    page = request.GET.get('page')
                    paged_products=paginetor.get_page(page)
                else:
                    products=Product.objects.filter(category=categories).order_by('-price')
                    count=products.count()
                    paginetor = Paginator(products,6)
                    page = request.GET.get('page')
                    paged_products=paginetor.get_page(page)
        if 'sorting' not in request.POST:
            if request.method=='POST':
                sort=request.POST['filtering']
                print("!!!!!!!!!")
                key=filter_price.objects.get(name=sort)              
                a=key.pricerange_from
                b=key.pricerange_to
                products = Product.objects.filter(category=categories,price__range=(a,b))
                paginator = Paginator(products,6)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
        if subcategory_slug != None:
            SubCategorys =get_object_or_404(SubCategory, slug=subcategory_slug)
            products = Product.objects.filter(SubCategory=SubCategorys, is_available=True)
            paginator = Paginator(products,6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            if 'filtering' not in request.POST:
                if request.method=='POST':
                    sort_id=request.POST['sorting']
                    if sort_id=='low':
                        products = Product.objects.filter(SubCategory=SubCategorys).order_by('price')
                        count=products.count()
                        paginetor = Paginator(products,6)
                        page = request.GET.get('page')
                        paged_products=paginetor.get_page(page)
                    else:
                        products = Product.objects.filter(SubCategory=SubCategorys).order_by('-price')
                        count=products.count()
                        paginetor = Paginator(products,6)
                        page = request.GET.get('page')
                        paged_products=paginetor.get_page(page)
            if 'filtering' in request.POST:
                if request.method=='POST':
                    sort=request.POST['filtering']
                    print("!!!!!!!!!")
                    key=filter_price.objects.get(name=sort)              
                    a=key.pricerange_from
                    b=key.pricerange_to
                    products = Product.objects.filter(SubCategory=SubCategorys,price__range=(a,b))
                    paginator = Paginator(products,6)
                    page = request.GET.get('page')
                    paged_products = paginator.get_page(page)
    else:
    
        products = Product.objects.all()
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        if 'filtering' in request.POST:
            if request.method=='POST':
                sort=request.POST['filtering']
                print("!!!!!!!!!")
                key=filter_price.objects.get(name=sort)              
                a=key.pricerange_from
                b=key.pricerange_to
                products = Product.objects.filter(price__range=(a,b))
                paginator = Paginator(products,6)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
        if 'filtering' not in request.POST:
            if request.method=='POST':                
                sort_id=request.POST['sorting']
                if sort_id=='low':
                    products = Product.objects.all().order_by('price')
                    count=products.count()
                    paginetor = Paginator(products,6)
                    page = request.GET.get('page')
                    paged_products=paginetor.get_page(page)
                else:
                    products = Product.objects.all().order_by('-price')
                    count=products.count()
                    paginetor = Paginator(products,6)
                    page = request.GET.get('page')
                    paged_products=paginetor.get_page(page)
    filtering=filter_price.objects.all()

    context = {
        'products': paged_products,
        'subcat': subcat,
        'product': product_count,
        'categories': categories,
        'filtering':filtering,
    }   
    return render(request, 'category.html', context) 

def productdetail(request, category_slug, subcategory_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, SubCategory__slug=subcategory_slug, slug=product_slug)
        related_product = Product.objects.filter(SubCategory__slug=subcategory_slug)
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user__id=request.user.id, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    #get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)
    reviwecount = ReviewRating.objects.filter(product_id=single_product.id,status=True).count()
    
    context = {
        'single_product': single_product,
        'related_product': related_product, 
        'orderproduct' : orderproduct,
        'reviews': reviews,
        'reviwecount':reviwecount,
    } 
    return render(request, 'product-detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-id').filter(Q(description__icontains= keyword) | Q(product_name__icontains= keyword) | Q(category__category_name__icontains= keyword) | Q(SubCategory__name__icontains= keyword) | Q(price__icontains= keyword))
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
    current_user  =  request.user
    product = Product.objects.get(id=product_id) # get the product   
    # if the user   is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            current_user  =  request.user
            
            for item in request.POST:
                print(item)
                key = item
                value = request.POST[key]
                

                try:
                    print("try One")
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    print(variation)
                    product_variation.append(variation)
                    print(product_variation)
                    # product_variation.reverse()
                    # print(product_variation)
                except:
                    pass
        
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
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
                if (product.stock - item.quantity)>0:
                    item.quantity += 1
                    item.save()  
                else:
                    messages.error(request,'No more stocks available!!') 
                    return redirect('cart')
            else:
                #create  a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    # if the user is not authenticated
    else:
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
                    print(product_variation)
                    # product_variation.reverse()
                    # print(product_variation)
                except:
                    pass
                
    
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
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
                if (product.stock - item.quantity)>0:
                    item.quantity += 1
                    item.save()  
                else:
                    messages.error(request,'No more stocks available!!') 
                    return redirect('cart')
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
                cart =cart )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
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
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item.delete()
    return redirect('cart')
    
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items =CartItem.objects.filter(user=request.user, is_active=True).filter().order_by('-id')
        else:
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

@login_required(login_url = 'login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        grand_total_without = 0
        discount=0
        start=0
        tax=0
        grand_total=0
        discount_price=0
        if request.user.is_authenticated:
            cart_items =CartItem.objects.filter(user=request.user, is_active=True)
            if request.method == 'POST':
                form = AddressForm(request.POST)
                if form.is_valid():
                    #store all the billing imformetions inserds the Order table
                    data = Address()
                    data.user = request.user
                    data.first_name = form.cleaned_data['first_name']
                    data.last_name = form.cleaned_data['last_name']
                    data.phone = form.cleaned_data['phone'] 
                    data.email = form.cleaned_data['email']
                    data.address_line_1 = form.cleaned_data['address_line_1']
                    data.address_line_2 = form.cleaned_data['address_line_2']
                    data.country = form.cleaned_data['country']
                    data.state = form.cleaned_data['state']
                    data.district = form.cleaned_data['district']
                    data.city = form.cleaned_data['city']
                    data.pincode = form.cleaned_data['pincode']
                    data.save()
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items =CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            address = Address.objects.filter(user=request.user)
            copeenn=Discount.objects.all()
            if request.method=='POST':
                checkd = Discount_coupon.objects.filter(user=request.user).exists()
                # checked = Discount.objects.get(discount_code=coupon)
                if checkd:
                    Discount_coupon.objects.filter(user=request.user).delete()
                   
                try:
                    coupon = request.POST['coupon']
                    checkd=Discount.objects.get(discount_code=coupon)
                    if checkd:
                        start =checkd.discount_from
                        discount = checkd.discount_percentage
                        print('checked'+ str(checkd))
                    else:
                        pass
                except:
                    tax = (2 * total)/100
                    grand_total_without = total + tax 
                    
            else:
                tax = (2 * total)/100
                grand_total_without = total + tax 
                
            
            tax= (2*total)/100
            grand_total= total + tax
            print(start)
            print(discount)
                        
            tax = (2 * total)/100
            grand_total_without = total + tax 
            print(quantity)
            try:
                if start:
                    if grand_total_without >= start:
                        discount_price =int(grand_total_without * discount / 100)   
                        grand_total =grand_total_without - discount_price
                        data =Discount_coupon()
                        data.user=request.user
                        data.discount_applied=discount_price
                        data.save()

            except:
                grand_total = int(grand_total_without)
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'address': address, 
        'discount_price': discount_price,
        'discount':copeenn,
       
    }
   
    return render(request, 'checkout.html',context)

def addwishlist(request, id):
    product= Product.objects.get(id=id)
    check = Wishlist.objects.filter(product=product).exists()
    
    if not check:
        wish = Wishlist()
        wish.user = request.user
        wish.product = product
        wish.save()

    return redirect('category') 
@login_required(login_url = 'login')
def wishlist(request):
    wishproducts = Wishlist.objects.filter(user=request.user)
    context ={
        'wishproducts': wishproducts,
    }
    return render(request, 'wishlist.html', context)
@login_required(login_url = 'login')
def wishlist_destroy(request, id):  
   wish = Wishlist.objects.get(id=id)  
   wish.delete()  
   return redirect("wishlist")  

def contact(request):
   return render(request,"contact.html") 

def about(request):  
    return render(request,"about.html") 

def review_submit(request,  product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews) 
            form.save()
            messages.success(request, 'Thank you! your review has been u  pdated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! your review has been Submited.')
                return redirect(url)
     