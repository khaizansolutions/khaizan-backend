# EXACT FIX FOR YOUR settings.py

# Find this section in your settings.py (around line 118):

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# REPLACE IT WITH THIS:

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'PAGE_SIZE_QUERY_PARAM': 'page_size',  # ⭐ ADD THIS LINE - Allows ?page_size=X in URL
    'MAX_PAGE_SIZE': 1000,  # ⭐ ADD THIS LINE - Maximum allowed page_size
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# That's it! Just add those 2 lines.

# After making this change:
# 1. Save the file
# 2. Restart your Django server
# 3. Test: https://khaizan-backend.onrender.com/api/products/?page_size=1000
# 4. You should now get all 104 products in one request

# What these lines do:
# - PAGE_SIZE_QUERY_PARAM: Allows frontend to control page size via URL
# - MAX_PAGE_SIZE: Sets maximum limit to 1000 (prevents abuse)