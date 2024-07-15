from django.db import models

# Create your models here.
from django.db import models

# create your models here


class Store(models.Model):
    ...


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
