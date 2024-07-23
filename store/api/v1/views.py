from rest_framework import generics
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from store import models

from .serializers import (
    AddCartItemSerializer, AllProductListSerializer, BaseProductAllProductListSerializer, 
    CartItemSerializer, CartSerialzier, CategoryProductSerializer, ChangeCartItemSerializer,
    CustomerSerializer, DateOrderSerializer, OrderCreateserializer, OrderSerializer, ProductCommentSerializer, ProductDetailSerializer, 
    HaghighyStoreSerializer, HoghoughyStoreSerializer, ProductListSerializer
)
from .filters import ProductFilter
from .permissions import ProductCommetPermission

# create your views here

class DateOrderViewSet(ModelViewSet):
    queryset = models.DateOrder.objects.all()
    serializer_class = DateOrderSerializer


class ProductCommentViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = models.ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [ProductCommetPermission]

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        base_product = models.Product.objects.get(slug=product_slug)

        return models.ProductComment.objects.filter(product_id=base_product.pk)
    
    def get_serializer_context(self):
        return {
            'product_slug': self.kwargs['product_slug'],
            'user': self.request.user 
        }


class AllProductListApiView(generics.ListAPIView):
    serializer_class = AllProductListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        pk=self.kwargs['pk']

        query = models.BaseProduct.objects.get(pk=pk)

        return Response({
            'base_product': BaseProductAllProductListSerializer(query, context={'base_product_id': pk}).data,
            # "seller_count": models.Store.objects.filter(products=query),
            'products': serializer.data
        })
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        base_product_obj = get_object_or_404(models.BaseProduct, pk=pk)
        queryset = models.ProductList.objects.filter(product__base_product__category=base_product_obj.category, product__base_product__sub_category=base_product_obj.sub_category)

        return queryset
    
    def get_serializer_context(self):
        return {'base_product_id': self.kwargs['pk']}


class CategoryViewSet(ModelViewSet):
    queryset = models.CategoryProduct.objects.all()
    serializer_class = CategoryProductSerializer
    lookup_field = 'slug'


class ProductViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = models.Product.objects.select_related('size').select_related('color') \
    .select_related('base_product__store').select_related('base_product__category') \
    .select_related('base_product__sub_category').prefetch_related(Prefetch(
        'property',
        queryset=models.SetProductProperty.objects.select_related('property')
    ))
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['product__sending_method', 'price', 'product__title_english']
    filterset_class = ProductFilter
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductDetailSerializer


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
        queryset=models.CartItem.objects.select_related('product__base_product')
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
        return models.CartItem.objects.filter(cart_id=cart_pk).select_related('product__base_product')
    

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
