from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Subcategory, Product, ProductImage
from .forms import ProductAdminForm


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'show_in_navbar',
        'navbar_order',
        'is_active',
        'created_at'
    )
    list_editable = ('show_in_navbar', 'navbar_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'show_in_navbar', 'created_at')
    ordering = ('navbar_order', 'name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'icon', 'description')
        }),
        ('Navigation Bar Settings', {
            'fields': ('show_in_navbar', 'navbar_order'),
            'description': 'Control how this category appears in the navigation bar.'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'slug',
        'is_active',
        'created_at'
    )
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    list_editable = ('is_active',)
    ordering = ('category__name', 'name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'icon', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'name',
        'sku',
        'brand',
        'product_type',
        'price',
        'stock_count',
        'in_stock',
        'is_active'
    )
    list_filter = (
        'product_type',
        'subcategory__category',
        'subcategory',
        'brand',
        'in_stock',
        'is_active',
        'is_featured',
        'created_at'
    )
    search_fields = (
        'name',
        'sku',
        'description',
        'brand',
        'subcategory__name',
        'subcategory__category__name'
    )
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_per_page = 25

    # Radio buttons for product type
    radio_fields = {'product_type': admin.HORIZONTAL}

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'subcategory', 'brand'),
            'classes': ('wide',)
        }),
        ('Product Type', {
            'fields': ('product_type',),
            'description': 'Select the type of product. Different fields will appear based on your selection.',
            'classes': ('wide',)
        }),
        ('Standard Pricing', {
            'fields': ('price', 'original_price', 'discount'),
            'description': 'Set the standard selling price and any discounts'
        }),
        ('📅 Rental Pricing (Only for Rental Products)', {
            'fields': (
                'rental_price_daily',
                'rental_price_weekly',
                'rental_price_monthly',
                'min_rental_period'
            ),
            'classes': ('collapse', 'rental-section'),
            'description': 'Set rental pricing options. At least one rental price is required for rental products.'
        }),
        ('🔧 Product Condition (For Refurbished Products)', {
            'fields': ('condition',),
            'classes': ('collapse', 'refurbished-section'),
            'description': 'Specify the condition of refurbished products (e.g., Excellent, Good, Fair)'
        }),
        ('Inventory', {
            'fields': ('stock_count', 'in_stock')
        }),
        ('Description & Media', {
            'fields': ('description', 'main_image'),
            'classes': ('wide',)
        }),
        ('✨ Product Features', {
            'fields': ('feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5'),
            'description': 'Enter key features of the product (one per field)',
            'classes': ('collapse',)
        }),
        ('📋 Specifications', {
            'fields': ('specifications_text',),
            'description': 'Enter technical specifications in "Key: Value" format, one per line',
            'classes': ('collapse',)
        }),
        ('Product Details', {
            'fields': ('weight', 'warranty_months'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Optimize for search engines'
        }),
        ('Ratings & Status', {
            'fields': ('rating', 'reviews', 'is_active', 'is_featured')
        }),
    )

    # Custom actions
    actions = [
        'mark_as_new',
        'mark_as_refurbished',
        'mark_as_rental',
        'mark_as_active',
        'mark_as_inactive'
    ]

    def mark_as_new(self, request, queryset):
        updated = queryset.update(product_type='new')
        self.message_user(request, f'{updated} product(s) marked as New Products')

    mark_as_new.short_description = '🆕 Mark as New Products'

    def mark_as_refurbished(self, request, queryset):
        updated = queryset.update(product_type='refurbished')
        self.message_user(request, f'{updated} product(s) marked as Refurbished Products')

    mark_as_refurbished.short_description = '🔧 Mark as Refurbished Products'

    def mark_as_rental(self, request, queryset):
        updated = queryset.update(product_type='rental')
        self.message_user(request, f'{updated} product(s) marked as Rental Products')

    mark_as_rental.short_description = '📅 Mark as Rental Products'

    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} product(s) marked as Active')

    mark_as_active.short_description = '✓ Mark as Active'

    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} product(s) marked as Inactive')

    mark_as_inactive.short_description = '✖ Mark as Inactive'

    class Media:
        js = ('admin/js/product_conditional_fields.js',)
        css = {
            'all': ('admin/css/product_admin.css',)
        }


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('is_primary', 'order')
    ordering = ('product', 'order')