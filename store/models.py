
from django.urls import reverse
from tkinter import CASCADE
from django.db import models

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
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('products_details',args=[self.category.slug,self.SubCategory.slug,self.slug])
    
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product
