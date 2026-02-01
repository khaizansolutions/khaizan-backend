from django.contrib import admin
from django.utils.html import format_html
from .models import QuoteRequest, QuoteItem


class QuoteItemInline(admin.TabularInline):
    """Inline admin for quote items"""
    model = QuoteItem
    extra = 0
    readonly_fields = ['subtotal_display']
    fields = ['product', 'quantity', 'price', 'subtotal_display']
    
    def subtotal_display(self, obj):
        if obj.id:
            return format_html('<strong>AED {:.2f}</strong>', obj.subtotal)
        return '-'
    subtotal_display.short_description = 'Subtotal'


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'phone',
        'company',
        'status',
        'items_count',
        'total_display',
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company', 'id']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'items_count', 'quantity_total', 'total_display']
    
    inlines = [QuoteItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Request Details', {
            'fields': ('message', 'status', 'admin_notes')
        }),
        ('Summary', {
            'fields': ('items_count', 'quantity_total', 'total_display'),
            'description': 'Quote summary (auto-calculated)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'
    
    def quantity_total(self, obj):
        return sum(item.quantity for item in obj.items.all())
    quantity_total.short_description = 'Total Quantity'
    
    def total_display(self, obj):
        total = sum(item.subtotal for item in obj.items.all())
        return format_html('<strong style="color: green; font-size: 16px;">AED {:.2f}</strong>', total)
    total_display.short_description = 'Total Amount'
    
    actions = ['mark_as_reviewing', 'mark_as_quoted', 'mark_as_completed']
    
    def mark_as_reviewing(self, request, queryset):
        queryset.update(status='reviewing')
        self.message_user(request, f'{queryset.count()} quotes marked as under review.')
    mark_as_reviewing.short_description = 'Mark as under review'
    
    def mark_as_quoted(self, request, queryset):
        queryset.update(status='quoted')
        self.message_user(request, f'{queryset.count()} quotes marked as quoted.')
    mark_as_quoted.short_description = 'Mark as quoted'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f'{queryset.count()} quotes marked as completed.')
    mark_as_completed.short_description = 'Mark as completed'