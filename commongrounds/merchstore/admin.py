from django.contrib import admin
from .models import ProductType, Product, Transaction


class ProductInLine(admin.TabularInline):
    model = Product


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    inline = [Product,]


class ProductAdmin(admin.ModelAdmin):
    model = Product
    search_fields = ('name', 'description', 'product_type__name')
    list_display = ('name', 'product_type', 'price')
    list_filter = ('product_type',)

    fieldsets = (
        ("Details", {
            "fields": ("name", "product_type", "description", "price")
        }),
    )


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ("buyer", "product", "amount", "status", "created_on")


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
