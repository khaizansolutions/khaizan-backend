# Backend: products/views.py

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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
    """
    queryset = Category.objects.filter(is_active=True).prefetch_related('subcategories')
    serializer_class = CategorySerializer
    lookup_field = 'slug'


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
    """
    queryset = Product.objects.filter(is_active=True).select_related('subcategory', 'subcategory__category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subcategory', 'subcategory__category', 'brand', 'in_stock', 'is_featured']
    search_fields = ['name', 'description', 'sku', 'brand']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        featured_products = self.queryset.filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)