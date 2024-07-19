import django_filters

from store.models import Product

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'slug': ['icontains'],
            'product__title_farsi': ['icontains']
        }
        