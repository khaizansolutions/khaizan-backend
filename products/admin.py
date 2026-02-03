# Backend: products/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage, Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('user', 'rating', 'comment', 'created_at')
    readonly_fields = ('created_at',)

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
    inlines = [ProductImageInline, ReviewInline]
    
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
            'description': 'Add detailed product description and main image'
        }),
        ('Features & Specifications', {
            'fields': ('features', 'specifications'),
            'description': '''
                <strong>Features:</strong> Enter as JSON list: ["Durable material", "Easy to use", "Long lasting"]<br>
                <strong>Specifications:</strong> Enter as JSON object: {"Weight": "500g", "Color": "Blue", "Material": "Plastic"}
            '''
        }),
        ('Ratings & Status', {
            'fields': ('rating', 'reviews', 'is_active')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'order', 'uploaded_at')
    list_filter = ('product',)
