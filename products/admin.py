# Backend: products/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'stock_count', 'in_stock', 'is_active')
    list_filter = ('category', 'in_stock', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand')
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
        ('Features & Specifications', {
            'fields': ('features', 'specifications'),
            'description': '<strong>Features:</strong> ["Feature 1", "Feature 2"]<br><strong>Specifications:</strong> {"Key": "Value"}'
        }),
        ('Ratings & Status', {
            'fields': ('rating', 'reviews', 'is_active')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'order')
    list_filter = ('product',)