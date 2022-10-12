from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('mlogin/', views.mlogin, name='mlogin'),
    path('mhome/', views.mhome, name='mhome'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('addsubcategory/', views.addsubcategory, name='addsubcategory'),
    path('category/', views.category, name='categoryz'),
    path('subcategory/', views.subcategory, name='subcategoryz'),
    path('cat_delete/<str:slug>/',views.cat_destroy, name='cat_delete'),
    path('editcat/<str:slug>/',views.editcat, name='editcat'),
    path('editsubcat/<str:slug>/',views.editsubcat, name='editsubcat'),
    path('subcat_delete/<str:slug>/',views.subcat_destroy, name='subcat_delete'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('product/', views.product, name='productz'),
    path('ajax/load-subcategory/', views.load_subcategory, name='ajax_load_subcategory'),
    path('productdelete/<str:slug>/',views.productdestroy, name='productdelete'),
    path('editproduct/<str:slug>/',views.editproduct, name='editproduct'),
    path('variation/', views.variationz, name='variationz'),
    path('addvariation/', views.addvariation, name='addvariation'),
    path('variationdestroy/<int:id>/',views.variationdestroy, name='variationdestroy'),
    path('editvariation/<int:id>/',views.editvariation, name='editvariation'),
    path('orderproduct/<int:order_id>/', views.orderproduct, name='orderproduct'),
    path('users/', views.users, name='users'),
    path('blockuser/<int:id>/', views.blockuser, name='blockuser'),
    path('order/', views.order, name='order'),
    path('orderstatus/<int:id>/', views.orderstatus, name='orderstatus'),
    path('user_mlogout/', views.user_mlogout, name='user_mlogout'),
    path('coupon/', views.coupon, name='coupon'),
    path('addcoupon/', views.addcoupon, name='addcoupon'),
    path('editcoupon/<int:id>/',views.editcoupon, name='editcoupon'),
    path('deletecoupon/<int:id>/',views.deletecoupon, name='deletecoupon'),
    path('addadmin',views.addadmin, name='addadmiin'),
    path('review',views.review, name='review'),
    path('review_destroy/<int:id>/',views.review_destroy, name='review_destroy'),
    path('pricefilter',views.pricefilter, name='pricefilter'),
    path('addpricefilter/', views.addpricefilter, name='addpricefilter'),
    path('deletefilter/<int:id>/',views.deletefilter, name='deletefilter'),
    path('editfilter/<int:id>/',views.editfilter, name='editfilter'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)