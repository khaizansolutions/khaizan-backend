from django.db import models
from products.models import Product

class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('sent', 'Sent'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Customer Info
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Quote #{self.id} - {self.name}"
    
    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())


class QuoteItem(models.Model):
    quote = models.ForeignKey(QuoteRequest, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"