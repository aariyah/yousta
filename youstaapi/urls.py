from django.urls import path
from youstaapi import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
router=DefaultRouter()
router.register("cloths",views.ClothViews,basename="cloths")

router.register("carts",views.CartView,basename="carts")

router.register("orders",views.OrderView,basename="orders")


urlpatterns=[

    path("register/",views.UserCreationView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
    
]+router.urls