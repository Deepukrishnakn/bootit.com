from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('place_order', views.place_order, name='place_order'),
    path('payment/', views.payment, name='payment'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)