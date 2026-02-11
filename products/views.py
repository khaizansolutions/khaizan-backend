# Backend: products/views.py

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView  # NEW: Added import
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404  # NEW: Added import
from .models import Category, Subcategory, Product
from .serializers import (
    CategorySerializer,
    SubcategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for categories
    GET /api/categories/ - List all categories with subcategories
    GET /api/categories/{id}/ - Get single category
    GET /api/categories/?navbar=true - Get only navbar categories (ordered by navbar_order)
    """
    queryset = Category.objects.filter(is_active=True).prefetch_related('subcategories')
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Optionally filter categories for navbar display
        """
        queryset = super().get_queryset()

        # Filter for navbar categories
        navbar = self.request.query_params.get('navbar', None)
        if navbar == 'true':
            queryset = queryset.filter(show_in_navbar=True).order_by('navbar_order')

        return queryset


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for subcategories
    GET /api/subcategories/ - List all subcategories
    GET /api/subcategories/{id}/ - Get single subcategory
    """
    queryset = Subcategory.objects.filter(is_active=True).select_related('category')
    serializer_class = SubcategorySerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for products
    GET /api/products/ - List all products
    GET /api/products/{id}/ - Get single product
    GET /api/products/featured/ - Get featured products
    GET /api/products/?product_type=new - Filter by product type (new/refurbished/rental)
    GET /api/products/?subcategory={id} - Filter by subcategory
    GET /api/products/?subcategory__category={id} - Filter by category
    """
    queryset = Product.objects.filter(is_active=True).select_related('subcategory', 'subcategory__category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'subcategory',
        'subcategory__category',
        'brand',
        'in_stock',
        'is_featured',
        'product_type'  # NEW: Filter by product type
    ]
    search_fields = ['name', 'description', 'sku', 'brand']
    ordering_fields = ['price', 'created_at', 'name', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        """
        Optionally filter products by product_type
        """
        queryset = super().get_queryset()

        # Filter by product type (new, refurbished, rental)
        product_type = self.request.query_params.get('product_type', None)
        if product_type:
            queryset = queryset.filter(product_type=product_type)

        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        featured_products = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def new(self, request):
        """Get new products"""
        new_products = self.queryset.filter(product_type='new')[:8]
        serializer = self.get_serializer(new_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def refurbished(self, request):
        """Get refurbished products"""
        refurbished_products = self.queryset.filter(product_type='refurbished')[:8]
        serializer = self.get_serializer(refurbished_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def rental(self, request):
        """Get rental products"""
        rental_products = self.queryset.filter(product_type='rental')[:8]
        serializer = self.get_serializer(rental_products, many=True)
        return Response(serializer.data)


# ============================================================================
# NEW: Custom Product Listing View for SEO-friendly URLs
# ============================================================================

class ProductListingView(APIView):
    """
    Handle three route types:
    1. /listing/new - Product type only
    2. /listing/category/office-supplies - Category only
    3. /listing/new/office-supplies - Product type + Category

    These routes provide clean, SEO-friendly URLs for product filtering.
    """

    def get(self, request, product_type=None, category_slug=None):
        """
        Handle all three route patterns with one method
        """
        # Get base queryset
        queryset = Product.objects.filter(is_active=True).select_related(
            'subcategory',
            'subcategory__category'
        )

        # Determine which filter to apply based on parameters
        if product_type and category_slug:
            # Route 3: Product-type + Category (/listing/new/office-supplies)
            return self._filter_by_type_and_category(queryset, product_type, category_slug)

        elif category_slug:
            # Route 2: Category only (/listing/category/office-supplies)
            return self._filter_by_category(queryset, category_slug)

        elif product_type:
            # Route 1: Product-type only (/listing/new)
            return self._filter_by_type(queryset, product_type)

        else:
            # Shouldn't happen with proper URL routing, but handle gracefully
            return Response(
                {'error': 'No filter provided'},
                status=400
            )

    def _filter_by_type(self, queryset, product_type):
        """
        Filter by product type only
        Example: /listing/new
        """
        # Validate product type
        valid_types = ['new', 'refurbished', 'rental']
        if product_type not in valid_types:
            return Response(
                {
                    'error': f'Invalid product type. Must be one of: {", ".join(valid_types)}'
                },
                status=404
            )

        # Filter products by type
        products = queryset.filter(product_type=product_type)
        serializer = ProductListSerializer(products, many=True)

        return Response({
            'products': serializer.data,
            'filter': {
                'type': 'product_type',
                'product_type': product_type
            },
            'count': products.count()
        })

    def _filter_by_category(self, queryset, category_slug):
        """
        Filter by category only (all product types)
        Example: /listing/category/office-supplies
        """
        # Find category (404 if not found)
        category = get_object_or_404(Category, slug=category_slug, is_active=True)

        # Get all subcategories under this category
        subcategory_ids = category.subcategories.filter(
            is_active=True
        ).values_list('id', flat=True)

        # Filter products by subcategory
        products = queryset.filter(subcategory_id__in=subcategory_ids)
        serializer = ProductListSerializer(products, many=True)

        return Response({
            'products': serializer.data,
            'category': CategorySerializer(category).data,
            'filter': {
                'type': 'category',
                'category_slug': category_slug
            },
            'count': products.count()
        })

    def _filter_by_type_and_category(self, queryset, product_type, category_slug):
        """
        Filter by both product type AND category
        Example: /listing/new/office-supplies
        """
        # Validate product type
        valid_types = ['new', 'refurbished', 'rental']
        if product_type not in valid_types:
            return Response(
                {
                    'error': f'Invalid product type. Must be one of: {", ".join(valid_types)}'
                },
                status=404
            )

        # Find category (404 if not found)
        category = get_object_or_404(Category, slug=category_slug, is_active=True)

        # Get all subcategories under this category
        subcategory_ids = category.subcategories.filter(
            is_active=True
        ).values_list('id', flat=True)

        # Filter by BOTH product type AND category
        products = queryset.filter(
            product_type=product_type,
            subcategory_id__in=subcategory_ids
        )
        serializer = ProductListSerializer(products, many=True)

        return Response({
            'products': serializer.data,
            'category': CategorySerializer(category).data,
            'filter': {
                'type': 'combined',
                'product_type': product_type,
                'category_slug': category_slug
            },
            'count': products.count()
        })