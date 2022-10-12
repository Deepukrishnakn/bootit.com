from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('place_order', views.place_order, name='place_order'),
    path('payment/', views.payment, name='payment'),
    path('razor_payments/', views.payment, name='razor_payments'),
    path('payment_status/', views.payment_status, name='payment_status'),
    path('cashon/', views.cashon, name='cashon'),
    path('cod_verify/', views.cod_verify, name='cod_verify'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)