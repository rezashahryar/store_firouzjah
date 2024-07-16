from rest_framework import serializers

from store import models

# create your serializers here


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Province
        fields = ['name']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ['name']


class MantagheSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Mantaghe
        fields = ['name']


class ProductPropertySerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()

    class Meta:
        model = models.SetProductProperty
        fields = ['property', 'value']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = [
            "title_farsi",
            "title_english",
            "category",
            "sub_category",
            "product_code",
            # "inventory",
            "product_model",
            "status_originaly",
            "product_warranty",
            "sending_method",
            "property"
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['property'] = ProductPropertySerializer(instance.property.all(), many=True).data

        return rep


class HaghighyStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HaghighyStore
        fields = [
            "name",
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
            "full_name",
            "birth_date",
            "name_father",
            "code_melli",
            "shomare_shenasname",
            "store_type",
        ]
        read_only_fields = ["code"]
        # extra_kwargs = {
        #     'name': {'required': True}
        # }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['province'] = ProvinceSerializer(instance.province).data
        rep['city'] = CitySerializer(instance.city).data
        rep['mantaghe'] = MantagheSerializer(instance.mantaghe).data
        return rep
    

class HoghoughyStoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.HoghoughyStore
        fields = [
            "name",
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
            "ceo_name",
            "company_name",
            "date_of_registration",
            "num_of_registration",
            "economic_code",
        ]
        read_only_fields = ["code"]
