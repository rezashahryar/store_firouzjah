from django.urls import path
from rest_framework_nested import routers

from . import views

# create your urls here

router = routers.DefaultRouter()
router.register('carts', views.CartViewSet, basename='cart')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('product/list/', views.ProductListApiView.as_view(), name='product_list'),
    path('store/create/', views.StoreCreateApiView.as_view(), name='store_create'),
]

urlpatterns += router.urls + cart_items_router.urls
