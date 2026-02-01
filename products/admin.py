from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images"""
    model = ProductImage
    extra = 3
    fields = ['image', 'alt_text', 'is_primary', 'order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'product_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'icon')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_thumbnail', 
        'name', 
        'sku', 
        'category', 
        'price',
        'stock_count', 
        'in_stock', 
        'is_featured',
        'created_at'
    ]
    list_filter = ['category', 'in_stock', 'is_featured', 'created_at', 'brand']
    search_fields = ['name', 'sku', 'brand', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['stock_count', 'in_stock', 'is_featured']
    date_hierarchy = 'created_at'
    
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount'),
            'description': 'Set the pricing details. Discount is calculated automatically.'
        }),
        ('Inventory', {
            'fields': ('stock_count', 'in_stock')
        }),
        ('Description & Details', {
            'fields': ('description', 'features', 'specifications'),
            'description': 'Features should be a list: ["Feature 1", "Feature 2"]. Specifications should be a dict: {"Key": "Value"}'
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Ratings & Reviews', {
            'fields': ('rating', 'reviews')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured'),
            'description': 'Active products are visible on site. Featured products show on homepage.'
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.main_image.url)
        return "No image"
    image_thumbnail.short_description = 'Image'
    
    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_in_stock', 'mark_out_of_stock']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} products marked as featured.')
    mark_as_featured.short_description = 'Mark selected as featured'
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} products removed from featured.')
    mark_as_not_featured.short_description = 'Remove from featured'
    
    def mark_in_stock(self, request, queryset):
        queryset.update(in_stock=True)
        self.message_user(request, f'{queryset.count()} products marked as in stock.')
    mark_in_stock.short_description = 'Mark as in stock'
    
    def mark_out_of_stock(self, request, queryset):
        queryset.update(in_stock=False)
        self.message_user(request, f'{queryset.count()} products marked as out of stock.')
    mark_out_of_stock.short_description = 'Mark as out of stock'