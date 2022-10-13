from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category, name='category'),
    path('category/<slug:category_slug>/', views.category, name='products_by_category'),    
    path('category/<slug:category_slug>/<slug:subcategory_slug>', views.category, name='products_by_subcategory'),
    path('category/ <slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.productdetail, name='products_details'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
