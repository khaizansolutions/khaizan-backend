from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


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

    # Navbar control fields
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
        indexes = [
            models.Index(fields=['show_in_navbar', 'navbar_order']),
            models.Index(fields=['is_active']),
        ]

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
        unique_together = ['category', 'name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class Product(models.Model):
    """Main Product Model"""

    # Product type choices
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

    # Product Type
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
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount percentage (0-100)"
    )

    # Rental Pricing (for rental products)
    rental_price_daily = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Daily rental price in AED"
    )
    rental_price_weekly = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weekly rental price in AED"
    )
    rental_price_monthly = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monthly rental price in AED"
    )
    min_rental_period = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Minimum rental period in days"
    )

    # Inventory
    stock_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Available quantity"
    )
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

    # Product Details
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kg"
    )
    warranty_months = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Warranty period in months"
    )
    condition = models.CharField(
        max_length=50,
        blank=True,
        help_text="Product condition (e.g., Excellent, Good, Fair for refurbished items)"
    )

    # Ratings & Reviews
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=4.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Average rating (0.0 - 5.0)"
    )
    reviews = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of reviews"
    )

    # Main Product Image
    main_image = models.ImageField(
        upload_to='products/%Y/%m/',
        blank=True,
        null=True,
        help_text="Main product image"
    )

    # SEO Fields
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="SEO title (leave blank to use product name)"
    )
    meta_description = models.TextField(
        max_length=500,
        blank=True,
        help_text="SEO meta description"
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
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['subcategory', 'is_active']),
            models.Index(fields=['product_type']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['brand']),
            models.Index(fields=['in_stock']),
        ]

    def clean(self):
        """Custom validation"""
        super().clean()

        # Validate rental prices for rental products
        if self.product_type == 'rental':
            if not any([self.rental_price_daily, self.rental_price_weekly, self.rental_price_monthly]):
                raise ValidationError({
                    'rental_price_daily': 'Rental products must have at least one rental price set.'
                })

        # Validate stock
        if self.in_stock and self.stock_count <= 0:
            raise ValidationError({
                'stock_count': 'Product marked as "in stock" must have stock_count > 0'
            })

        # Validate discount logic
        if self.discount > 0 and not self.original_price:
            raise ValidationError({
                'original_price': 'Original price must be set when discount is applied'
            })

        if self.original_price and self.price > self.original_price:
            raise ValidationError({
                'price': 'Discounted price cannot be higher than original price'
            })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Auto-set meta_title if empty
        if not self.meta_title:
            self.meta_title = self.name

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
        if self.discount > 0 and self.original_price:
            discount_amount = (self.original_price * self.discount) / 100
            return round(self.original_price - discount_amount, 2)
        return self.price

    @property
    def discount_amount(self):
        """Calculate actual discount amount in AED"""
        if self.discount > 0 and self.original_price:
            return round(self.original_price - self.price, 2)
        return 0

    @property
    def is_on_sale(self):
        """Check if product is currently on sale"""
        return self.discount > 0 and self.original_price is not None

    @property
    def stock_status(self):
        """Get stock status as string"""
        if self.stock_count == 0:
            return "Out of Stock"
        elif self.stock_count < 5:
            return "Low Stock"
        else:
            return "In Stock"

    @property
    def product_type_display(self):
        """Get human-readable product type"""
        return dict(self.PRODUCT_TYPE_CHOICES).get(self.product_type, 'New Product')

    def get_primary_image(self):
        """Get primary product image or main_image"""
        primary = self.images.filter(is_primary=True).first()
        return primary.image if primary else self.main_image

    def get_all_images(self):
        """Get all product images including main_image"""
        images = list(self.images.all())
        if self.main_image and not images:
            return [self.main_image]
        return images


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
    order = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Display order"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        indexes = [
            models.Index(fields=['product', 'is_primary']),
            models.Index(fields=['product', 'order']),
        ]

    def save(self, *args, **kwargs):
        # Auto-set alt_text if empty
        if not self.alt_text:
            self.alt_text = f"{self.product.name} - Image {self.order}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"