from django.contrib import admin

from store import models

# Register your models here.


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    ...


@admin.register(models.CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(models.SubCategoryProduct)
class SubCategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title_english', )}


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    ...


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Mantaghe)
class MantagheAdmin(admin.ModelAdmin):
    ...
