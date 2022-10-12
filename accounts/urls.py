from django.conf import settings
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('otp/', views.otp, name='otp'),
    path('login/', views.login, name='login'),
    path('logout/',views.user_logout,name='logout'),
    # path('home/', views.home, name='home'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    #path('active/<uidb64>/', views.activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('my_order/', views.my_order, name='my_order'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 