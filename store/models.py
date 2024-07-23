import random

from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# create your models here


class Color(models.Model):
    name = models.CharField(max_length=255)
    code_of_color = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Mantaghe(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

def random_code_store():

    while True:
        code = random.randint(100000, 999999)

        if Store.objects.filter(code=code).exists():
            continue
        return code


class Store(models.Model):

    class StoreType(models.TextChoices):
        HAGHIGHY = "ha", _("حقیقی")
        HOGHOUGHY = "ho", _("حقوقی")

    name = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    code = models.CharField(max_length=6, unique=True, default=random_code_store)
    
    shomare_shaba = models.CharField(max_length=26)

    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='stores')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='stores')
    mantaghe = models.ForeignKey(Mantaghe, on_delete=models.CASCADE, related_name='stores')
    mahalle = models.CharField(max_length=255)

    address = models.CharField(max_length=555)
    post_code = models.CharField(max_length=10)

    parvane_kasb = models.FileField(upload_to='parvane_kasb__/%Y/%m/%d/')
    tasvire_personely = models.ImageField(upload_to='tasvire_personely__/%Y/%m/%d/')
    kart_melli = models.ImageField(upload_to='kart_melli__/%Y/%m/%d/')
    shenasname = models.ImageField(upload_to='tasvire_shenasname__/%Y/%m/%d/')
    logo = models.ImageField(upload_to='logo__/%Y/%m/%d/')
    roozname_rasmi_alamat = models.FileField(upload_to='roozname_rasmi_alamat__/%Y/%m/%d/')

    gharardad = models.FileField(upload_to='gharardad__/%Y/%m/%d/')

    store_type = models.CharField(max_length=2, choices=StoreType.choices)

    def __str__(self):

        if self.name:
            return str(self.name)
        else:
            return str(self.mobile_number)


class HaghighyStore(Store):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    name_father = models.CharField(max_length=255)
    code_melli = models.CharField(max_length=10, unique=True)
    shomare_shenasname = models.CharField(max_length=255)

    def __str__(self):
        return str(self.full_name)


class HoghoughyStore(Store):
    ceo_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    date_of_registration = models.DateField()
    num_of_registration = models.CharField(max_length=255)
    economic_code = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name
    
class ProductProperties(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class SetProductProperty(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='property')
    property = models.ForeignKey(ProductProperties, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f'property {self.property} for {self.product} with value {self.value}'


class CategoryProduct(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images/%Y/%m/%d/')
    slug = models.SlugField()

    def __str__(self):
        return self.name
    

class SubCategoryProduct(models.Model):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='sub_categories', null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name
    

class ProductType(models.Model):
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products_type')
    sub_category = models.ForeignKey(SubCategoryProduct, on_delete=models.CASCADE, related_name='products_type')

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

def random_code_product():

    while True:
        code = random.randint(1000, 9999)

        if Store.objects.filter(code=code).exists():
            continue
        return code
    

class Size(models.Model):
    size = models.CharField(max_length=11)

    def __str__(self):
        return self.size


class BaseProduct(models.Model):

    class StatusOriginaly(models.TextChoices):
        ORIGINAL = "o", _("اصل ، اوریجینال")

    class SendingMethod(models.TextChoices):
        PISHTAZ = "pish", _("پیشتاز")
        TIPAX = "tip", _("تیپاکس")
        BAARBARY = "bar", _("باربری")
        PEYK_MOTOR = "peyk", _("پیک موتوری")

    class ProductStatus(models.TextChoices):
        CONFIRM = 'c', _('تایید شده')
        WAITING = 'w', _('در انتظار تایید')
        NOT_CONFIRM = 'n', _('تایید نشده')

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')

    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubCategoryProduct, on_delete=models.CASCADE, related_name='products')

    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, related_name='products', null=True)

    title_farsi = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255)

    description = models.TextField()

    product_model = models.CharField(max_length=255)

    status_originaly = models.CharField(max_length=10, choices=StatusOriginaly.choices)
    product_warranty = models.BooleanField()

    sending_method = models.CharField(max_length=4, choices=SendingMethod.choices)

    product_status = models.CharField(max_length=1, choices=ProductStatus.choices, default=ProductStatus.WAITING)

    def __str__(self):
        return self.title_farsi
    

class Product(models.Model):

    class ProductUnit(models.TextChoices):
        PAIR = "p", _("جفت")
        NUM = "n", _("عددی")

    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='products')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='products')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='products')
    inventory = models.PositiveIntegerField()
    unit = models.CharField(max_length=3, choices=ProductUnit.choices)

    product_code = models.CharField(max_length=4, unique=True, default=random_code_product)

    slug = models.SlugField()

    price = models.IntegerField()
    price_after_discount = models.IntegerField(null=True)
    discount_percent = models.PositiveIntegerField(null=True)

    start_discount_datetime = models.DateTimeField(null=True)
    end_discount_datetime = models.DateTimeField(null=True)

    length_package = models.IntegerField(null=True, blank=True)
    width_package = models.IntegerField(null=True, blank=True)
    height_package = models.IntegerField(null=True, blank=True)
    weight_package = models.IntegerField(null=True, blank=True)

    shenase_kala = models.CharField(max_length=14)
    barcode = models.CharField(max_length=16)

    def __str__(self):
        return self.base_product.title_farsi
    

class ProductList(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_list')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_lists')
    

class ProductImage(models.Model):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=r'product_images/%Y/%m/%d/')
    is_cover = models.BooleanField()

    def __str__(self):
        return self.product.title_farsi
    

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customers')
    receiver_full_name = models.CharField(max_length=255)
    recevier_mobile = models.CharField(max_length=11)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='customers')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='customers')
    mantaghe = models.ForeignKey(Mantaghe, on_delete=models.CASCADE, related_name='customers')
    mahalle = models.CharField(max_length=11)
    pelak = models.CharField(max_length=11)
    vahed = models.CharField(max_length=3)
    code_posti = models.CharField(max_length=12)
    refferer_code = models.CharField(max_length=255)


    def __str__(self):
        if self.receiver_full_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return str(self.user)
        

class TimeOrder(models.Model):
    time_from = models.TimeField()
    time_until = models.TimeField()

    def __str__(self):
        return str(f'{self.time_from} {self.time_until}')


class DateOrder(models.Model):
    date = models.DateField() 
    time = models.ManyToManyField(TimeOrder, related_name='dates')

    def __str__(self):
        return str(f'{self.date}: ')


class UnpaidOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)
    

class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_CANCELED, 'Canceled')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)

    date_order = models.ForeignKey(DateOrder, on_delete=models.CASCADE, related_name='orders')
    time_order = models.ForeignKey(TimeOrder, on_delete=models.CASCADE, related_name='orders')

    # unpaid_orders = UnpaidOrderManager()

    def __str__(self):
        return f'Order id = {self.pk}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    unit_price = models.IntegerField()

    class Meta:
        unique_together = [['order', 'product']]


class ProductComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    

class RequestPhotografy(models.Model):
    full_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=11)

    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='request_photografy')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='request_photografy')
    mantaghe = models.ForeignKey(Mantaghe, on_delete=models.CASCADE, related_name='request_photografy')
    mahalle = models.CharField(max_length=255)

    address = models.TextField()
    store_name = models.CharField(max_length=255)

    request_text = models.TextField()
