from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

# create your urls here

router = DefaultRouter()
router.register('carts', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet, basename='customer')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('product/list/', views.ProductListApiView.as_view(), name='product_list'),
    path('store/create/', views.StoreCreateApiView.as_view(), name='store_create'),
]

urlpatterns += router.urls + cart_items_router.urls
