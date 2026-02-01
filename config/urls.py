from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



# Customize admin site
admin.site.site_header = "Khaizen Solutions Admin"
admin.site.site_title = "Khaizen Admin"
admin.site.index_title = "Welcome to Khaizen Solutions Dashboard"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('quotes.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)