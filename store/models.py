
from django.urls import reverse
from django.db import models
from django.db.models import Avg,Count
from accounts.models import Account

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = 'categrory'
        verbose_name_plural = 'categories'
        
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])    
    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    def get_url(self):
        return reverse('products_by_subcategory',args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.category.category_name+'/'+self.name


class filter_price(models.Model): 
    name = models.CharField(max_length=50) 
    pricerange_from = models.IntegerField()
    pricerange_to = models.IntegerField()
    
    def __str__(self):
        return self.name
        
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    image1 = models.ImageField(upload_to='photos/products')
    image2 = models.ImageField(upload_to='photos/products')
    image3 = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    # price_range = models.ForeignKey(filter_price, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('products_details',args=[self.category.slug,self.SubCategory.slug,self.slug])
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average']) 
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count =Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count']) 
        return count
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category= 'color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category= 'size', is_active=True)
    
Variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
 )
    
class Variation(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=Variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)
    created_on         = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value
    
class Cart(models.Model):
    cart_id = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product

class Discount(models.Model):
    discount_code = models.CharField(max_length=20)
    discount_percentage = models.FloatField()
    discount_from = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.discount_code
    
class Discount_coupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2)

    
class Wishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class ReviewRating(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE )
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject