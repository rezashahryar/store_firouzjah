from rest_framework import generics

from store import models

from .serializers import ProductSerializer

# create your views here


class ProductListApiView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
