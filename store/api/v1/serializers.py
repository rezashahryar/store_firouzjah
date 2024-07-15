from rest_framework import serializers

from store import models

# create your serializers here


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = ['title_farsi', 'title_english', 'category', 'product_code', 'product_model', 'status_originaly', 'product_warranty', 'sending_method']
