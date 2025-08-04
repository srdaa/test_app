from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'orders', OrderViewSet, basename="order")

urlpatterns = [
    path('buy/items/<int:item_id>/', BuyItemView.as_view()),
    path('buy/orders/<int:order_id>', BuyOrderView.as_view()),
    path('paid/<int:order_id>', OrderPaidView.as_view()),
    path('', include(router.urls))
]