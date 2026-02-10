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
    list_display = ('name', 'slug', 'subcategory_count', 'show_in_navbar', 'navbar_order', 'is_active')
    list_editable = ('show_in_navbar', 'navbar_order')  # Edit directly in list view
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'show_in_navbar', 'created_at')
    ordering = ('navbar_order', 'name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'icon', 'description')
        }),
        ('Navbar Settings', {
            'fields': ('show_in_navbar', 'navbar_order'),
            'description': 'Control whether this category appears in the navigation bar and its display order'
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
    ordering = ('category__name', 'name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'icon', 'description')
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
    list_display = (
        'name',
        'sku',
        'get_category',
        'subcategory',
        'brand',
        'product_type',  # NEW: Show product type
        'price',
        'stock_count',
        'in_stock',
        'is_active'
    )
    list_filter = (
        'product_type',  # NEW: Filter by product type
        'subcategory__category',
        'subcategory',
        'in_stock',
        'is_active',
        'is_featured',
        'created_at'
    )
    search_fields = ('name', 'sku', 'description', 'brand', 'subcategory__name', 'subcategory__category__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    # Radio buttons for product type instead of dropdown
    radio_fields = {'product_type': admin.HORIZONTAL}

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'subcategory', 'brand')
        }),
        ('Product Type', {
            'fields': ('product_type',),
            'description': 'Select product type: New, Refurbished, or Rental',
            'classes': ('wide',)
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
            'fields': ('rating', 'reviews', 'is_active', 'is_featured')
        }),
    )

    def get_category(self, obj):
        return obj.subcategory.category.name if obj.subcategory else '-'

    get_category.short_description = 'Category'
    get_category.admin_order_field = 'subcategory__category__name'

    # Add custom actions for bulk operations
    actions = ['mark_as_new', 'mark_as_refurbished', 'mark_as_rental']

    def mark_as_new(self, request, queryset):
        updated = queryset.update(product_type='new')
        self.message_user(request, f'{updated} products marked as New Products')

    mark_as_new.short_description = 'Mark selected as New Products'

    def mark_as_refurbished(self, request, queryset):
        updated = queryset.update(product_type='refurbished')
        self.message_user(request, f'{updated} products marked as Refurbished Products')

    mark_as_refurbished.short_description = 'Mark selected as Refurbished Products'

    def mark_as_rental(self, request, queryset):
        updated = queryset.update(product_type='rental')
        self.message_user(request, f'{updated} products marked as Rental Products')

    mark_as_rental.short_description = 'Mark selected as Rental Products'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'order', 'created_at')
    list_filter = ('product', 'created_at')
    ordering = ('product', 'order')