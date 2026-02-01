from rest_framework import serializers
from .models import QuoteRequest, QuoteItem
from products.serializers import ProductListSerializer


class QuoteItemSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = QuoteItem
        fields = ['id', 'product', 'product_details', 'quantity', 'price', 'subtotal']


class QuoteRequestSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = QuoteRequest
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'message',
            'items', 'total_amount', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        quote = QuoteRequest.objects.create(**validated_data)
        
        for item_data in items_data:
            QuoteItem.objects.create(quote=quote, **item_data)
        
        return quote