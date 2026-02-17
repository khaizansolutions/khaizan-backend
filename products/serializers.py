from rest_framework import serializers
import cloudinary
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
            'show_in_navbar', 'navbar_order'
        ]

    def get_product_count(self, obj):
        total = 0
        for subcategory in obj.subcategories.all():
            total += subcategory.products.filter(is_active=True).count()
        return total


class ProductImageSerializer(serializers.ModelSerializer):
    # ⭐ FIX: Convert CloudinaryField to full URL
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']

    def get_image(self, obj):
        if obj.image:
            return cloudinary.CloudinaryImage(str(obj.image)).build_url()
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for Product List - minimal fields for performance"""
    category_name = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    product_type_display = serializers.CharField(read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_on_sale = serializers.BooleanField(read_only=True)
    stock_status = serializers.CharField(read_only=True)
    # ⭐ FIX: Convert CloudinaryField to full URL
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'category_name', 'subcategory_name',
            'brand', 'product_type', 'product_type_display',
            'price', 'original_price', 'discount', 'final_price', 'is_on_sale',
            'main_image', 'stock_count', 'stock_status', 'in_stock',
            'rating', 'reviews', 'is_featured'
        ]

    def get_main_image(self, obj):
        if obj.main_image:
            return cloudinary.CloudinaryImage(str(obj.main_image)).build_url()
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for Product Detail - all fields"""
    category_name = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    subcategory = SubcategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    product_type_display = serializers.CharField(read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_on_sale = serializers.BooleanField(read_only=True)
    stock_status = serializers.CharField(read_only=True)
    # ⭐ FIX: Convert CloudinaryField to full URL
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            # Basic Info
            'id', 'name', 'slug', 'sku', 'category_name', 'subcategory_name',
            'subcategory', 'brand', 'product_type', 'product_type_display',

            # Pricing
            'price', 'original_price', 'discount', 'final_price', 'discount_amount', 'is_on_sale',

            # Rental Pricing
            'rental_price_daily', 'rental_price_weekly', 'rental_price_monthly', 'min_rental_period',

            # Images
            'main_image', 'images',

            # Inventory
            'stock_count', 'stock_status', 'in_stock',

            # Description
            'description', 'features', 'specifications',

            # Product Details
            'weight', 'warranty_months', 'condition',

            # Ratings
            'rating', 'reviews',

            # SEO
            'meta_title', 'meta_description',

            # Status
            'is_featured', 'created_at'
        ]

    def get_main_image(self, obj):
        if obj.main_image:
            return cloudinary.CloudinaryImage(str(obj.main_image)).build_url()
        return None