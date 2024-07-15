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


class AbstractStore(models.Model):
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

    parvane_kasb = models.FileField(upload_to=f'parvane_kast__{mobile_number}/%Y/%m/%d/')
    tasvire_personely = models.ImageField(upload_to=f'tasvire_personely__{mobile_number}/%Y/%m/%d/')
    kart_melli = models.ImageField(upload_to=f'kart_melli__{mobile_number}/%Y/%m/%d/')
    shenasname = models.ImageField(upload_to=f'tasvire_shenasname__{mobile_number}/%Y/%m/%d/')
    logo = models.ImageField(upload_to=f'logo__{mobile_number}/%Y/%m/%d/')
    roozname_rasmi_alamat = models.FileField(upload_to=f'roozname_rasmi_alamat__{mobile_number}/%Y/%m/%d/')

    gharardad = models.FileField(upload_to=f'gharardad__{mobile_number}/%Y/%m/%d/')

    class Meta:
        abstract = True


class Store(AbstractStore):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


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
