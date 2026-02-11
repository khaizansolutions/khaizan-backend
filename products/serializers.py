# Backend: products/serializers.py

from rest_framework import serializers
from .models import Category, Subcategory, Product, ProductImage


class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'icon', 'description', 'category_name', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'icon', 'description',
            'subcategories', 'product_count',
            'show_in_navbar', 'navbar_order'  # NEW: Navbar fields
        ]

    def get_product_count(self, obj):
        # Count all products across all subcategories
        total = 0
        for subcategory in obj.subcategories.all():
            total += subcategory.products.filter(is_active=True).count()
        return total


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    product_type_display = serializers.CharField(read_only=True)  # NEW: Human-readable product type

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'category_name', 'subcategory_name',
            'brand', 'product_type', 'product_type_display',  # NEW: Added product_type fields
            'price', 'original_price', 'discount', 'main_image',
            'stock_count', 'in_stock', 'rating', 'reviews', 'is_featured'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    subcategory = SubcategorySerializer(read_only=True)  # NEW: Full subcategory details
    images = ProductImageSerializer(many=True, read_only=True)
    product_type_display = serializers.CharField(read_only=True)  # NEW: Human-readable product type

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'category_name', 'subcategory_name',
            'subcategory',  # NEW: Full subcategory object with category info
            'brand', 'product_type', 'product_type_display',  # NEW: Added product_type fields
            'price', 'original_price', 'discount', 'main_image',
            'images', 'stock_count', 'in_stock', 'description', 'features',
            'specifications', 'rating', 'reviews', 'is_featured', 'created_at'
        ]