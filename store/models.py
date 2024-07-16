import random

from django.db import models
from django.utils.translation import gettext_lazy as _

# create your models here

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
    

def random_code():

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
    code = models.CharField(max_length=6, unique=True, default=random_code)
    
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


class Product(models.Model):

    class StatusOriginaly(models.TextChoices):
        ORIGINAL = "o", _("اصل ، اوریجینال")

    class SendingMethod(models.TextChoices):
        PISHTAZ = "pish", _("پیشتاز")
        TIPAX = "tip", _("تیپاکس")
        BAARBARY = "bar", _("باربری")
        PEYK_MOTOR = "peyk", _("پیک موتوری")

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')

    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubCategoryProduct, on_delete=models.CASCADE, related_name='products')

    title_farsi = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255)

    slug = models.SlugField()
    
    product_code = models.CharField(max_length=100)
    product_model = models.CharField(max_length=255)

    status_originaly = models.CharField(max_length=10, choices=StatusOriginaly.choices)
    product_warranty = models.BooleanField()

    sending_method = models.CharField(max_length=4, choices=SendingMethod.choices)

    def __str__(self):
        return self.title_farsi
