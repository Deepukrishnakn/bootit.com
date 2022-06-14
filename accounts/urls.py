from django.conf import settings

from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('otp/', views.otp, name='otp'),
    path('login/', views.login, name='login'),
    # path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    #path('active/<uidb64>/', views.activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 