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


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Color
        fields = ['name', 'code_of_color']


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Store
        fields = ['name', 'code']


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = ['image', 'is_cover']


class BaseProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()
    store = StoreSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = models.BaseProduct
        fields = [
            'store', 'category', 'sub_category', 'title_farsi', 'title_english', 'description',
            'slug', 'product_code', 'product_model', 'status_originaly',
            'product_warranty', 'sending_method', 'images',
        ]


class ProductSerializer(serializers.ModelSerializer):
    product = BaseProductSerializer()
    size = serializers.StringRelatedField()
    color = ColorSerializer()

    class Meta:
        model = models.Product
        fields = [
            'product', 'size', 'color', 'inventory', 'unit', 'price', 'price_after_discount',
            'discount_percent', 'start_discount_datetime', 'end_discount_datetime',
            'length_package', 'width_package', 'height_package', 'weight_package',
            'shenase_kala', 'barcode',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['property'] = ProductPropertySerializer(instance.property.all(), many=True).data

        return rep


class HaghighyStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HaghighyStore
        fields = [
            "name", "mobile_number", "phone_number", "email", "shomare_shaba", "province",
            "city", "mantaghe", "mahalle", "address", "post_code", "parvane_kasb",
            "tasvire_personely", "kart_melli", "shenasname", "logo", "roozname_rasmi_alamat",
            "gharardad", "code", "full_name", "birth_date",
            "name_father", "code_melli", "shomare_shenasname", "store_type",
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
            "name", "mobile_number", "phone_number", "email", "shomare_shaba", "province",
            "city", "mantaghe", "mahalle", "address", "post_code", "parvane_kasb",
            "tasvire_personely", "kart_melli", "shenasname", "logo", "roozname_rasmi_alamat",
            "gharardad", "code", "ceo_name", "company_name", "date_of_registration",
            "num_of_registration", "economic_code",
        ]
        read_only_fields = ["code"]


class CartBaseProductserializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseProduct
        fields = ['title_farsi']


class ChangeCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = ['quantity']


class AddCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_pk = self.context['cart_pk']

        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cart_item = models.CartItem.objects.get(cart_id=cart_pk, product_id=product)
            cart_item.quantity += quantity
            cart_item.save()
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(cart_id=cart_pk, quantity=validated_data['quantity'], product=validated_data['product'].pk)

        self.instance = cart_item
        return cart_item


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ['product', 'price']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product'] = CartBaseProductserializer(instance.product).data

        return rep


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price


class CartSerialzier(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']

    def get_total_price(self, cart):
        return sum(item.quantity * item.product.price for item in cart.items.all())
