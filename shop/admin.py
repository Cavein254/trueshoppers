from django.contrib import admin

from products.models import Product

from .models import Shop


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ("name", "price", "stock_quantity", "sku")
    readonly_fields = "sku"


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__email")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductInline]
