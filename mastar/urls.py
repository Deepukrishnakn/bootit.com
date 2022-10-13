from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register('allvendor',views.AllVenderViewset,basename="allvendor")
router.register('alluser',views.AllUserViewset,basename="alluser")
router.register('userorders',views.UserOrderViewset,basename="userorders")
router.register('vendororders',views.VendorOrderViewset,basename="vendororders")
urlpatterns = [
    path('Activetvendor/<int:id>/', views.ActivetVendor, name="Activetvendor"),
    path('Orderchart/', views.Orderchart, name="Orderchart"),
       
 ]+router.urls 