from rest_framework import serializers

from store import models

# create your serializers here


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = [
            "title_farsi",
            "title_english",
            "category",
            "product_code",
            "product_model",
            "status_originaly",
            "product_warranty",
            "sending_method",
        ]


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Store
        fields = [
            "mobile_number",
            "phone_number",
            "email",
            "shomare_shaba",
            "province",
            "city",
            "mantaghe",
            "mahalle",
            "address",
            "post_code",
            "parvane_kasb",
            "tasvire_personely",
            "kart_melli",
            "shenasname",
            "logo",
            "roozname_rasmi_alamat",
            "gharardad",
            "code",
        ]
        read_only_fields = ["code"]
