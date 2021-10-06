from django.contrib import admin

from mainapp.models import Product, ProductCategory

# Register your models here.


admin.site.register(ProductCategory)
# admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'is_active')
    fields = (('name', 'is_active'), 'image', 'description', ('price', 'quantity'), 'category')
    readonly_fields = ('description',)
    ordering = ('name', 'price')
    search_fields = ('name',)
