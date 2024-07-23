from django.urls import path
from rest_framework_nested import routers

from . import views

# create your urls here

router = routers.DefaultRouter()
router.register('carts', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
router.register('comments', views.ProductCommentViewSet, basename='product_comment')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('comments', views.ProductCommentViewSet, basename='product-comment')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('product/list/<int:pk>/', views.AllProductListApiView.as_view(), name='product_list'),
    path('store/create/', views.StoreCreateApiView.as_view(), name='store_create'),
    path('order/list/', views.OrderListApiView.as_view(), name='order'),
    path('order/create/', views.OrderCreateApiView.as_view(), name='order_create'),
]

urlpatterns += router.urls + cart_items_router.urls + product_router.urls
