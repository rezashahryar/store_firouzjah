from rest_framework import serializers

from django.db import transaction

from core.models import User
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


class ProductCommentUserSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_info']

    def get_user_info(self, product_comment_user):
        if product_comment_user.mobile:
            return str(product_comment_user.mobile)
        else:
            return str(product_comment_user.username)
        

class ProductCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductComment
        fields = ['id', 'text', 'datetime_created']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = ProductCommentUserSerializer(instance.user).data

        return rep
    
    def create(self, validated_data):
        product_slug = self.context['product_slug']
        base_product = models.Product.objects.get(slug=product_slug)

        return models.ProductComment.objects.create(
            product_id=base_product.pk,
            user=self.context['user'],
            **validated_data
        )


class BaseProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()
    store = StoreSerializer()
    images = ProductImageSerializer(many=True)

    status_originaly = serializers.CharField(source='get_status_originaly_display')
    sending_method = serializers.CharField(source='get_sending_method_display')

    comments = ProductCommentSerializer(many=True)

    class Meta:
        model = models.BaseProduct
        fields = [
            'id', 'store', 'category', 'sub_category', 'title_farsi', 'title_english', 'description',
            'product_model', 'status_originaly',
            'product_warranty', 'sending_method', 'images', 'comments'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    base_product = BaseProductSerializer()
    size = serializers.StringRelatedField()
    color = ColorSerializer()

    unit = serializers.CharField(source='get_unit_display')

    class Meta:
        model = models.Product
        fields = [
            'id', 'base_product', 'size', 'color', 'inventory', 'unit', 'price', 'price_after_discount',
            'discount_percent', 'start_discount_datetime', 'end_discount_datetime',
            'length_package', 'width_package', 'height_package', 'weight_package',
            'shenase_kala', 'barcode',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['property'] = ProductPropertySerializer(instance.property.all(), many=True).data

        return rep
    

class BaseProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()

    class Meta:
        model = models.BaseProduct
        fields = ['category', 'sub_category', 'title_farsi']
    

class ProductListSerializer(serializers.ModelSerializer):
    base_product = BaseProductListSerializer()
    unit = serializers.CharField(source='get_unit_display')

    class Meta:
        model = models.Product
        fields = ['base_product', 'slug', 'price', 'price_after_discount', 'start_discount_datetime', 'end_discount_datetime', 'unit']


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


class StoreDetailAllProductListSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()

    class Meta:
        model = models.Store
        fields = ['code', 'province']


class ProductDetailAllProductListSerializer(serializers.ModelSerializer):
    title_farsi = serializers.CharField(source='base_product.title_farsi')

    class Meta:
        model = models.Product
        fields = ['title_farsi', 'price', 'price_after_discount', 'discount_percent']


class BaseProductAllProductListSerializer(serializers.ModelSerializer):
    seller_count = serializers.SerializerMethodField()
    cheapest_price = serializers.SerializerMethodField()
    most_expensive_price = serializers.SerializerMethodField()

    class Meta:
        model = models.BaseProduct
        fields = ['title_farsi', 'title_english', 'seller_count', 'cheapest_price', 'most_expensive_price']

    def get_seller_count(self, base_product):
        obj = models.BaseProduct.objects.get(pk=self.context['base_product_id'])
        return models.Store.objects.all().filter(products__category=obj.category, products__sub_category=obj.sub_category).count()
    
    def get_cheapest_price(self, base_product):
        obj = models.BaseProduct.objects.get(pk=self.context['base_product_id'])
        queryset = models.Product.objects.filter(base_product__category=obj.category, base_product__sub_category=obj.sub_category).order_by('price')

        if queryset:
            return queryset[0].price
        return None
    
    def get_most_expensive_price(self, base_product):
        obj = models.BaseProduct.objects.get(pk=self.context['base_product_id'])
        queryset = models.Product.objects.filter(base_product__category=obj.category, base_product__sub_category=obj.sub_category).order_by('-price')

        if queryset:
            return queryset[0].price
        # elif obj is not None:
        #     return models.Product.objects.get(product__title_farsi__icontains=obj.title_farsi).price
        return None


class AllProductListSerializer(serializers.ModelSerializer):
    store = StoreDetailAllProductListSerializer()
    product = ProductDetailAllProductListSerializer()


    class Meta:
        model = models.ProductList
        fields = ['store', 'product']


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
        fields = ['slug', 'price', 'price_after_discount']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['base_product'] = CartBaseProductserializer(instance.base_product).data

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
    total_discount_price = serializers.SerializerMethodField()
    amount_payable = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price', 'total_discount_price', 'amount_payable']
        read_only_fields = ['id']

    def get_total_price(self, cart):
        return sum(item.quantity * item.product.price for item in cart.items.all())
    
    def get_total_discount_price(self, cart):
        x = sum(item.product.price_after_discount for item in cart.items.all())
        return x
    
    def get_amount_payable(self, cart):
        for item in cart.items.all():
            if item.product.discount_percent:
                result = self.get_total_price(cart) - sum(item.quantity * item.product.price_after_discount for item in cart.items.all())
                return result
            result = self.get_total_price(cart) - sum(item.quantity * item.product.price for item in cart.items.all())
        return result
    

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = ['first_name', 'last_name', 'user']


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ['id', 'base_product', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ['id', 'customer_id', 'status', 'datetime_created', 'items']


class OrderCreateserializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not models.Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError("there is not such cart")
        
        if models.CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("your cart is empty")
        
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']

            customer = models.Customer.objects.get(user_id=user_id)

            order = models.Order()
            order.customer = customer
            order.save()

            cart_items = models.CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = list()

            for item in cart_items:
                order_item = models.OrderItem()
                order_item.order = order
                order_item.product = item.product
                order_item.unit_price = item.product.price
                order_item.quantity = item.quantity

                order_items.append(order_item)
            
            models.OrderItem.objects.bulk_create(order_items)

            models.Cart.objects.get(id=cart_id).delete()

            return order
        

class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CategoryProduct
        fields = ['name', 'image', 'slug']
