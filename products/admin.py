from django.contrib import admin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "price", "stock_quantity")
    list_filter = ("shop", "category")
    search_fields = ("name", "sku")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
