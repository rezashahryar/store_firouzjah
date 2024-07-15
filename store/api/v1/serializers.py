from rest_framework import serializers

from store import models

# create your serializers here


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ['title_farsi', 'title_english']
