from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Subcategory, Product
from .serializers import (
    CategorySerializer,
    SubcategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer
)


class StandardPagination(PageNumberPagination):
    page_size = 20               # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100          # ⭐ Hard cap — prevents 1000-item requests killing Render


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True).prefetch_related('subcategories')
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subcategory.objects.filter(is_active=True).select_related('category')
    serializer_class = SubcategorySerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Product.objects
        .filter(is_active=True)
        .select_related('subcategory', 'subcategory__category')  # ⭐ Prevents N+1
        .prefetch_related('images')                               # ⭐ Prevents N+1 on images
        .only(                                                    # ⭐ Only fetch needed fields for list
            'id', 'name', 'slug', 'sku', 'brand',
            'product_type', 'price', 'original_price', 'discount',
            'main_image', 'stock_count', 'in_stock',
            'rating', 'reviews', 'is_featured',
            'subcategory', 'created_at'
        )
    )
    lookup_field = 'slug'
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subcategory', 'subcategory__category', 'brand', 'in_stock', 'is_featured', 'product_type']
    search_fields = ['name', 'description', 'sku', 'brand']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        # For detail view, fetch ALL fields
        if self.action == 'retrieve':
            return (
                Product.objects
                .filter(is_active=True)
                .select_related('subcategory', 'subcategory__category')
                .prefetch_related('images')
            )
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = (
            Product.objects
            .filter(is_active=True, is_featured=True)
            .select_related('subcategory', 'subcategory__category')
            [:6]
        )
        serializer = ProductListSerializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def new(self, request):
        products = (
            Product.objects
            .filter(is_active=True, product_type='new')
            .select_related('subcategory', 'subcategory__category')
            [:8]
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def refurbished(self, request):
        products = (
            Product.objects
            .filter(is_active=True, product_type='refurbished')
            .select_related('subcategory', 'subcategory__category')
            [:8]
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def rental(self, request):
        products = (
            Product.objects
            .filter(is_active=True, product_type='rental')
            .select_related('subcategory', 'subcategory__category')
            [:8]
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)