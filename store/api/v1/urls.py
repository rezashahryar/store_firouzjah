from django.urls import path

from . import views

# create your urls here

urlpatterns = [
    path('product/list/', views.ProductListApiView.as_view(), name='product_list'),
    path('store/create/', views.StoreCreateApiView.as_view(), name='store_create'),
]
