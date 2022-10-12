from django.contrib import admin
from .models import Address, Payment,Order, OrderProduct

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'order_total', 'tax', 'is_ordered', 'created_at']
    list_filter = ['is_ordered']
    seaech_field = ['order_numbeer', 'first_name', 'last_name']
    list_per_page = 20





admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Address)