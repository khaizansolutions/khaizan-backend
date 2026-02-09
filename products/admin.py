# Backend: products/admin.py

from django.contrib import admin
from .models import Category, Subcategory, Product, ProductImage
from .forms import ProductAdminForm


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'subcategory_count', 'is_active', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def subcategory_count(self, obj):
        return obj.subcategories.count()

    subcategory_count.short_description = 'Subcategories'
    subcategory_count.admin_order_field = 'subcategories__count'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'product_count', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category__name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Products'
    product_count.admin_order_field = 'products__count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'sku', 'get_category', 'subcategory', 'price', 'stock_count', 'in_stock', 'is_active')
    list_filter = ('subcategory__category', 'subcategory', 'in_stock', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description', 'brand', 'subcategory__name', 'subcategory__category__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'subcategory', 'brand')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount')
        }),
        ('Inventory', {
            'fields': ('stock_count', 'in_stock')
        }),
        ('Description', {
            'fields': ('description', 'main_image'),
        }),
        ('Features', {
            'fields': ('feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5'),
            'description': 'Enter each feature in a separate field'
        }),
        ('Specifications', {
            'fields': ('specifications_text',),
            'description': 'Enter each specification on a new line: Key: Value'
        }),
        ('Ratings & Status', {
            'fields': ('rating', 'reviews', 'is_active')
        }),
    )

    def get_category(self, obj):
        return obj.subcategory.category.name if obj.subcategory else '-'

    get_category.short_description = 'Category'
    get_category.admin_order_field = 'subcategory__category__name'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'order')
    list_filter = ('product',)