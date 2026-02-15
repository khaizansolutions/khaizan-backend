from django import forms
from django.core.exceptions import ValidationError
from .models import Product
import json


class ProductAdminForm(forms.ModelForm):
    """Custom form for Product admin with dynamic fields based on product type"""

    # Feature fields (converts JSON list to individual fields)
    feature_1 = forms.CharField(max_length=500, required=False, label="Feature 1")
    feature_2 = forms.CharField(max_length=500, required=False, label="Feature 2")
    feature_3 = forms.CharField(max_length=500, required=False, label="Feature 3")
    feature_4 = forms.CharField(max_length=500, required=False, label="Feature 4")
    feature_5 = forms.CharField(max_length=500, required=False, label="Feature 5")

    # Specifications as text area (converts JSON dict to text)
    specifications_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        required=False,
        label="Specifications",
        help_text="Enter each specification on a new line in format: Key: Value<br>Example:<br>Weight: 1.5kg<br>Dimensions: 30x20x10cm<br>Color: Black"
    )

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 80}),
            'meta_description': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate feature fields from JSON
        if self.instance.pk and self.instance.features:
            features = self.instance.features if isinstance(self.instance.features, list) else []
            for i, feature in enumerate(features[:5], 1):
                field_name = f'feature_{i}'
                if field_name in self.fields:
                    self.initial[field_name] = feature

        # Populate specifications text from JSON
        if self.instance.pk and self.instance.specifications:
            specs = self.instance.specifications if isinstance(self.instance.specifications, dict) else {}
            specs_text = '\n'.join([f"{k}: {v}" for k, v in specs.items()])
            self.initial['specifications_text'] = specs_text

        # Add CSS classes for conditional display
        # Rental-specific fields
        rental_fields = [
            'rental_price_daily',
            'rental_price_weekly',
            'rental_price_monthly',
            'min_rental_period'
        ]
        for field in rental_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['class'] = 'rental-field'

        # Refurbished-specific field
        if 'condition' in self.fields:
            self.fields['condition'].widget.attrs['class'] = 'refurbished-field'
            self.fields['condition'].help_text = "Required for refurbished products (e.g., Excellent, Good, Fair)"

    def clean(self):
        cleaned_data = super().clean()
        product_type = cleaned_data.get('product_type')

        # Validate rental products must have at least one rental price
        if product_type == 'rental':
            rental_daily = cleaned_data.get('rental_price_daily')
            rental_weekly = cleaned_data.get('rental_price_weekly')
            rental_monthly = cleaned_data.get('rental_price_monthly')

            if not any([rental_daily, rental_weekly, rental_monthly]):
                raise ValidationError(
                    "Rental products must have at least one rental price (daily, weekly, or monthly)."
                )

        # Validate refurbished products should have condition
        if product_type == 'refurbished':
            condition = cleaned_data.get('condition')
            if not condition:
                self.add_error('condition', 'Condition is recommended for refurbished products')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert feature fields to JSON list
        features = []
        for i in range(1, 6):
            feature = self.cleaned_data.get(f'feature_{i}', '').strip()
            if feature:
                features.append(feature)
        instance.features = features

        # Convert specifications text to JSON dict
        specs_text = self.cleaned_data.get('specifications_text', '').strip()
        specifications = {}
        if specs_text:
            for line in specs_text.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    specifications[key.strip()] = value.strip()
        instance.specifications = specifications

        if commit:
            instance.save()

        return instance

    class Media:
        js = ('admin/js/product_conditional_fields.js',)
        css = {
            'all': ('admin/css/product_admin.css',)
        }