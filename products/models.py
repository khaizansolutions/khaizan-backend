from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Main Product Categories like Office Supplies, Technology, etc."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name from lucide-react (e.g., 'Package', 'Printer')"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # NEW: Navbar control fields
    show_in_navbar = models.BooleanField(
        default=False,
        help_text="Display this category in the navigation bar"
    )
    navbar_order = models.IntegerField(
        default=0,
        help_text="Display order in navbar (1, 2, 3, etc.). 0 = not shown"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['navbar_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Subcategories under main categories (e.g., Pens, Calculators under Stationery)"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, max_length=250)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        help_text="Parent category"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name from lucide-react"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Subcategories"
        ordering = ['category__name', 'name']
        unique_together = ['category', 'name']  # Same subcategory name allowed under different categories

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class Product(models.Model):
    """Main Product Model"""

    # NEW: Product type choices
    PRODUCT_TYPE_CHOICES = [
        ('new', 'New Product'),
        ('refurbished', 'Refurbished Product'),
        ('rental', 'Rental Product'),
    ]

    # Basic Information
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=350)
    sku = models.CharField(max_length=100, unique=True, help_text="Stock Keeping Unit")
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name='products',
        help_text="Product subcategory"
    )
    brand = models.CharField(max_length=200)

    # NEW: Product Type
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='new',
        help_text="Select product type: New, Refurbished, or Rental"
    )

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Current selling price in AED"
    )
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original price before discount"
    )
    discount = models.IntegerField(
        default=0,
        help_text="Discount percentage (0-100)"
    )

    # Inventory
    stock_count = models.IntegerField(default=0, help_text="Available quantity")
    in_stock = models.BooleanField(default=True)

    # Description & Details
    description = models.TextField(help_text="Main product description")
    features = models.JSONField(
        null=True,
        default=list,
        blank=True,
        help_text='List of features: ["Feature 1", "Feature 2"]'
    )
    specifications = models.JSONField(
        default=dict,
        blank=True,
        help_text='Specifications: {"Weight": "1kg", "Color": "Black"}'
    )

    # Ratings & Reviews
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=4.5,
        help_text="Average rating (0.0 - 5.0)"
    )
    reviews = models.IntegerField(default=0, help_text="Number of reviews")

    # Main Product Image
    main_image = models.ImageField(
        upload_to='products/%Y/%m/',
        blank=True,
        null=True,
        help_text="Main product image"
    )

    # Status Flags
    is_active = models.BooleanField(default=True, help_text="Is product visible?")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage?")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def category(self):
        """Get parent category through subcategory"""
        return self.subcategory.category if self.subcategory else None

    @property
    def final_price(self):
        """Calculate price after discount"""
        if self.original_price and self.discount > 0:
            return self.price
        return self.price

    @property
    def product_type_display(self):
        """Get human-readable product type"""
        return dict(self.PRODUCT_TYPE_CHOICES).get(self.product_type, 'New Product')


class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/%Y/%m/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"