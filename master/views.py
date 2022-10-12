from multiprocessing import context
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import datetime
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from store.models import ReviewRating
from store.models import Category,SubCategory,Product,Variation,Discount,filter_price
from django.contrib import auth,messages
from .forms import categoryform, productform,subcategoryform, usersform,variationform,orderform,couponform,filterform
from orders.models import OrderProduct,Order
from django.db.models.functions import ExtractMonth
from django.db.models import Max,Min,Avg,Count
from accounts.models import Account
from django.db.models import Q
import calendar
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

a=Account.objects.filter(is_superadmin=True)


def mlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password') 
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_superadmin:
                login(request,user)
                return redirect('mhome')
        else:
            messages.error(request, 'invalid credientiail')
            return redirect('mlogin')
    return render(request, 'master/mlogin.html')

@user_passes_test(lambda u: u in a, login_url='mlogin')
def addcategory(request):
    form = categoryform()
    if request.method == 'POST':
        form = categoryform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    context ={
        'form':form
    }   
    return render(request, 'master/addcategory.html', context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def addsubcategory(request):
    form = subcategoryform()
    if request.method == 'POST':
        form = subcategoryform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    context ={
        'form':form
    }   
    return render(request, 'master/addsubcategory.html', context)
@user_passes_test(lambda u: u in a, login_url='mlogin')

def category(request):    
    category = Category.objects.all()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            category=Category.objects.filter(Q(category_name__icontains=keyword))
    context ={'category':category}
    return render(request, 'master/category.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def subcategory(request):
    subcategory = SubCategory.objects.all()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            subcategory = SubCategory.objects.filter(Q(name__icontains=keyword))
    context ={'subcategory':subcategory}
    return render(request, 'master/subcategory.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def product(request):
    product = Product.objects.all()
    paginator = Paginator(product,5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = product.count()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.filter(Q(description__icontains= keyword) | Q(product_name__icontains= keyword) | Q(category__category_name__icontains= keyword))
    context ={'product':product_count,
              'products': paged_products}
    return render(request, 'master/product.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def load_subcategory(request):
    category_id = request.GET.get('category')
    print(category_id)
    subcategory = SubCategory.objects.filter(category_id=category_id).order_by('name')
    print(subcategory)
    return render(request, 'master/subcatdrowpdown.html', {'SubCategory': subcategory})

@user_passes_test(lambda u: u in a, login_url='mlogin')
def cat_destroy(request, slug):  
   category = Category.objects.get(slug=slug)  
   category.delete()  
   return redirect("categoryz")  

@user_passes_test(lambda u: u in a, login_url='mlogin')
def editcat(request, slug):
    category = Category.objects.get(slug=slug)
    form= categoryform(instance=category) 
    if request.method == 'POST':
        form = categoryform (request.POST,request.FILES,instance=category)
        if form.is_valid():
            form.save()
            return redirect('categoryz')
    context = {
        'form':form,
        }
    return render(request, 'master/edit_cat.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def mhome(request):
    orders = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    users = Account.objects.filter(is_superadmin=False).count()
    totalproducts = Product.objects.all().count()
    totalorders = Order.objects.all().count()
    print(users)
    
    today = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    products = Product.objects.all()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-id').filter(Q(description__icontains= keyword) | Q(product_name__icontains= keyword) | Q(category__category_name__icontains= keyword))

    customers_verified = Account.objects.filter(is_admin=False,is_active = True)
    customers_unverified = Account.objects.filter(is_admin=False,is_active = False)
    number_customer = int(customers_verified.count() + customers_unverified.count())
    cdata = [customers_verified.count(),customers_unverified.count()]
    clabel = ['Verified','Unverified']
    
    context = {
        'monthNumber':monthNumber,
        'totalOrders':totalOrders,
        'users':users,
        'totalproducts': totalproducts,
        'totalorders': totalorders,
        'today':today,
        'products':products,
        'number_customer':number_customer,
        'cdata':cdata,
        'clabel':clabel,
    }
    return render(request, 'master/mhome.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def subcat_destroy(request, slug):  
   Subcategory = SubCategory.objects.get(slug=slug)  
   Subcategory.delete()  
   return redirect("subcategory")  

@user_passes_test(lambda u: u in a, login_url='mlogin')
def editsubcat(request, slug):
    subcategory = SubCategory.objects.get(slug=slug)
    form= subcategoryform(instance=subcategory) 
    if request.method == 'POST':
        form = subcategoryform (request.POST,request.FILES,instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('subcategoryz')
    context = {
        'form':form,
        }
    return render(request, 'master/editsubcat.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def addproduct(request):
    form = productform()
    if request.method == 'POST':
        form = productform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('productz')
    context ={
        'form':form,
    }   
    return render(request, 'master/addproduct.html', context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def editproduct(request, slug):
    product = Product.objects.get(slug=slug)
    form= productform(instance=product) 
    if request.method == 'POST':
        form = productform (request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('productz')
    context = {
        'form':form,
        }
    return render(request, 'master/edit_product.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def productdestroy(request, slug):  
   product = Product.objects.get(slug=slug)  
   product.delete()  
   return redirect("productz")

@user_passes_test(lambda u: u in a, login_url='mlogin')
def variationz(request):
    variation = Variation.objects.all().order_by('-id')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            variation = Variation.objects.filter(Q(variation_category__icontains=keyword) | Q(variation_value__icontains=keyword))
    paginator = Paginator(variation,5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = variation.count()
    
    context ={'variation':paged_products,
              'product':product_count}
    return render(request, 'master/variation.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def variationdestroy(request, id):  
   variation = Variation.objects.get(id=id)  
   variation.delete()  
   return redirect("variationz")

@user_passes_test(lambda u: u in a, login_url='mlogin')
def editvariation(request, id):
    variation = Variation.objects.get(id=id)
    form= variationform(instance=variation) 
    if request.method == 'POST':
        form = variationform (request.POST,request.FILES,instance=variation)
        if form.is_valid():
            form.save()
            return redirect('variationz')
    context = {
        'form':form,
        }
    return render(request, 'master/editvariation.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def addvariation(request):
    form = variationform()
    if request.method == 'POST':
        form = variationform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    context ={
        'form':form
    }   
    return render(request, 'master/addvariation.html', context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def orderproduct(request, order_id):
    orderproduct = OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            orderproduct = OrderProduct.objects.filter(Q(product__product_name__icontains=keyword) | Q(Variation__variations__icontains=keyword))
    context ={'orderproduct':orderproduct,
              'order':order}
    return render(request, 'master/orderproduct.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def users(request):
    users = Account.objects.all().order_by('-id')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users = Account.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))
    paginator = Paginator(users,5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = users.count()
    
    context ={'users':paged_products,
              'product':product_count}
    return render(request, 'master/users.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def blockuser(request, id):
    users = Account.objects.get(id=id)
    if users.is_active:
        users.is_active= False
        users.save()
    else:
        users.is_active= True
        users.save()
    return redirect('users')

@user_passes_test(lambda u: u in a, login_url='mlogin')
def order(request):
    order = Order.objects.all().order_by('-id')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            order = Order.objects.filter(Q(order_number__icontains=keyword) | Q(user__first_name__icontains=keyword))
    paginator = Paginator(order,5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = order.count()
    context ={'order':paged_products,
              'product':product_count}
    return render(request, 'master/order.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def orderstatus(request, id):
    orderstatus = Order.objects.get(id=id)
    form= orderform(instance=orderstatus) 
    if request.method == 'POST':
        form = orderform (request.POST,request.FILES,instance=orderstatus)
        if form.is_valid():
            form.save()
            return redirect('order')
    context = {
        'form':form,
        }
    return render(request, 'master/orderstatus.html',context)

def user_mlogout(request):
   if 'm_user' in request.session:
      request.session.flush()
   logout(request)
   messages.success(request, 'You Were Logged Out')
   return redirect('mlogin')

@user_passes_test(lambda u: u in a, login_url='mlogin')
def coupon(request):
    coupon = Discount.objects.all().order_by('-id')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            coupon = Discount.objects.filter(Q(discount_code__icontains=keyword) | Q(discount_percentage__icontains=keyword) | Q(discount_from__icontains=keyword))
    context ={'coupon':coupon}
    return render(request, 'master/coupon.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def addcoupon(request):
    form = couponform()
    if request.method == 'POST':
        form = couponform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    context ={
        'form':form
    } 
    return render(request, 'master/addcoupon.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def editcoupon(request, id):
    coupon = Discount.objects.get(id=id)
    form= couponform(instance=coupon) 
    if request.method == 'POST':
        form = couponform (request.POST,instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupon')
    context = {
        'form':form,
        }
    return render(request, 'master/editcoupon.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def deletecoupon(request, id):  
   coupon = Discount.objects.get(id=id)  
   coupon.delete()  
   return redirect("coupon")

@user_passes_test(lambda u: u in a, login_url='mlogin')
def addadmin(request):
    form = usersform()
    if request.method == 'POST':
        form = usersform(request.POST)
        if form.is_valid():
            form.save()
    context ={
        'form':form
    }   
    return render(request, 'master/addadmin.html', context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def review(request):
    reviews = ReviewRating.objects.all().order_by('-id')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            reviews = ReviewRating.objects.filter(Q(product__product_name__icontains=keyword) | Q(user__first_name__icontains=keyword) | Q(subject__icontains=keyword) | Q(rating__icontains=keyword))
    paginator = Paginator(reviews,5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = reviews.count()
    context ={'reviews':paged_products,
              'product':product_count,}
    return render(request, 'master/review.html',context)

@user_passes_test(lambda u: u in a, login_url='mlogin')
def review_destroy(request, id):  
   review = ReviewRating.objects.get(id=id)  
   review.delete()  
   return redirect("review")  


def pricefilter(request):
    filters = filter_price.objects.all().order_by('-id')
    paginator = Paginator(filters,2)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = filters.count()
    context={
        'filters':paged_products,
        'product':product_count,
    }
    return render(request, 'master/pricefilter.html',context)

def addpricefilter(request):
    form = filterform()
    if request.method == 'POST':
        form = filterform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('pricefilter')
    context ={
        'form':form
    } 
    return render(request, 'master/addpricefilter.html',context)


def deletefilter(request, id):  
    filter = filter_price.objects.get(id=id)  
    filter.delete()  
    return redirect("pricefilter")


def editfilter(request, id):
    filter = filter_price.objects.get(id=id)
    form= filterform(instance=filter) 
    if request.method == 'POST':
        form = filterform (request.POST,instance=filter)
        if form.is_valid():
            form.save()
            return redirect('pricefilter')
    context = {
        'form':form,
        }
    return render(request, 'master/editfilter.html',context)