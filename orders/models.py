
from django.db import models
from accounts.models import Account
from store.models import Product,Variation

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    account_paid = models. CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100,blank=True )
    paid= models.BooleanField(default=False) 
    
    def __str__(self):
        return self.payment_id 
    
class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __ste__(self):
        return self.first_name
    
class Order(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Out_For_Delivery', 'Out_For_Delivery'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
    )
    
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField(null=True)
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.address.first_name
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __ste__(self):
        return self.product.product_name

