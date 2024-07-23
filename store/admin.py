from django.contrib import admin

from store import models

# Register your models here.


@admin.register(models.ProductComment)
class CommentProduct(admin.ModelAdmin):
    ...


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    ...


@admin.register(models.HaghighyStore)
class HaghighyStoreAdmin(admin.ModelAdmin):
    ...


@admin.register(models.HoghoughyStore)
class HoghoughyStoreAdmin(admin.ModelAdmin):
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


@admin.register(models.BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title_english', )}
    ...


@admin.register(models.ProductList)
class ProductListAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    ...


@admin.register(models.TimeOrder)
class TimeOrderAdmin(admin.ModelAdmin):
    ...


@admin.register(models.DateOrder)
class DateOrderAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    ...


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    fields = ['product', 'quantity']
    extra = 1
    min_num = 1


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline
    ]


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Mantaghe)
class MantagheAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductProperties)
class ProductPropertiesAdmin(admin.ModelAdmin):
    ...


@admin.register(models.SetProductProperty)
class SetProductPropertiesAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    ...
