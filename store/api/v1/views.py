from rest_framework import generics
from django.db.models import Prefetch

from store import models

from .serializers import ProductSerializer, HaghighyStoreSerializer, HoghoughyStoreSerializer

# create your views here


class ProductListApiView(generics.ListAPIView):
    queryset = models.Product.objects.select_related('category').prefetch_related(Prefetch(
        'property',
        queryset=models.SetProductProperty.objects.select_related('property')
    )).all()
    serializer_class = ProductSerializer


class StoreCreateApiView(generics.CreateAPIView):
    queryset = models.Store.objects.all()

    def get_serializer_class(self):
        if self.request.data['store_type'] == 'ha':
            return HaghighyStoreSerializer
        elif self.request.data['store_type'] == 'ho':
            return HoghoughyStoreSerializer
