from django.db import models
from django.utils.translation import gettext_lazy as _

# create your models here


class Store(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class CategoryProduct(models.Model):
    name = models.CharField(max_length=255)
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
