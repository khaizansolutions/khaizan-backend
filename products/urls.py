# Backend: products/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    SubcategoryViewSet,
    ProductViewSet,
    ProductListingView  # NEW: Import the new view
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # ========================================================================
    # NEW: Custom product listing routes for SEO-friendly URLs
    # IMPORTANT: These MUST come BEFORE router.urls to avoid conflicts
    # ========================================================================

    # Route 2: Category only
    # Example: /api/listing/category/office-supplies
    path('listing/category/<slug:category_slug>/',
         ProductListingView.as_view(),
         name='product-listing-category'),

    # Route 3: Product-type + Category (combined filter)
    # Example: /api/listing/new/office-supplies
    path('listing/<str:product_type>/<slug:category_slug>/',
         ProductListingView.as_view(),
         name='product-listing-type-category'),

    # Route 1: Product-type only
    # Example: /api/listing/new
    path('listing/<str:product_type>/',
         ProductListingView.as_view(),
         name='product-listing-type'),

    # ========================================================================
    # Existing ViewSet routes (keep these - they still work)
    # ========================================================================
    path('', include(router.urls)),
]