
from accounts.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view,authentication_classes
from django.core.mail import send_mail
from accounts.models import Account
from accounts.serializers import RegisterSerializer
from payments.serializers import OrderSerializer
from payments.models import Order
from vendor.serializers import VendorRegisterSerializer,VendorOrderSerializer
from .serializer import VendorActivatSerializer
from rest_framework.response import Response
from vendor.models import Vendor,VendorOrder
from rest_framework import viewsets
from django.db.models.functions import ExtractMonth
import calendar
from django.db.models import Count

# Create your views here.

@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def ActivetVendor(request, id):
    vendor = Vendor.objects.get(id=id)
    change = VendorActivatSerializer(instance=vendor, data=request.data)
    if change.is_valid():
        change.save()
    else:
        change.save()
    send_mail('Hello  ',
                'Thank You For Join with Jogobonito ,Your Application is Aproved,  You can apost and manage your turf.',
                'deepukrishna25@gmail.com'
                ,[vendor.email]   
                ,fail_silently=False)
    return Response(change.data)

@authentication_classes([JWTAuthentication])
class AllVenderViewset(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorRegisterSerializer


@authentication_classes([JWTAuthentication])
class AllUserViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer


@authentication_classes([JWTAuthentication])
class UserOrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@authentication_classes([JWTAuthentication])
class VendorOrderViewset(viewsets.ModelViewSet):
    queryset = VendorOrder.objects.all()
    serializer_class = VendorOrderSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def Orderchart(request):
    monthNumber=0
    totalOrders=0
    orders = Order.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count')
    totalusers = Account.objects.filter(is_admin=False,is_active = True).count()
    totalvendor = Vendor.objects.filter(is_active = True).count()
    print(totalusers)
    print(totalvendor)
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])

    formdata ={
        'monthNumber':monthNumber,
        'totalOrders':totalOrders,
        'totalusers':totalusers,
        'totalvendor':totalvendor,
    }
    return Response(formdata)