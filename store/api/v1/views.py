from rest_framework import generics
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from django.db.models import Prefetch

from store import models

from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerialzier, ChangeCartItemSerializer, CustomerSerializer, OrderCreateserializer, OrderSerializer, ProductSerializer, HaghighyStoreSerializer, HoghoughyStoreSerializer

# create your views here


class ProductListApiView(generics.ListAPIView):
    queryset = models.Product.objects.select_related('size').select_related('color') \
    .select_related('product__store').select_related('product__category') \
    .select_related('product__sub_category').prefetch_related(Prefetch(
        'property',
        queryset=models.SetProductProperty.objects.select_related('property')
    ))
    serializer_class = ProductSerializer


class StoreCreateApiView(generics.CreateAPIView):
    queryset = models.Store.objects.all()

    def get_serializer_class(self):
        if self.request.data['store_type'] == 'ha':
            return HaghighyStoreSerializer
        elif self.request.data['store_type'] == 'ho':
            return HoghoughyStoreSerializer
        

class CartViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = models.Cart.objects.prefetch_related(Prefetch(
        'items',
        queryset=models.CartItem.objects.select_related('product__product')
    )).all()
    serializer_class = CartSerialzier


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_context(self):
        cart_pk = self.kwargs['cart_pk']
        return {'cart_pk': cart_pk}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return ChangeCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return models.CartItem.objects.filter(cart_id=cart_pk).select_related('product__product')
    

class CustomerViewSet(ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderListApiView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.pk}

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return OrderCreateserializer

    def get_queryset(self):
        queryset = models.Order.objects.prefetch_related('items__product')

        if self.request.user.is_staff:
            return queryset
        
        return queryset.filter(customer__user_id=self.request.user.pk)
    

class OrderCreateApiView(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = OrderCreateserializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.pk}
