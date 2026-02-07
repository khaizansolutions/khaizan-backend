# Backend: products/forms.py

from django import forms
from .models import Product
import json

class ProductAdminForm(forms.ModelForm):
    # Features as separate fields
    feature_1 = forms.CharField(max_length=200, required=False, label="Feature 1")
    feature_2 = forms.CharField(max_length=200, required=False, label="Feature 2")
    feature_3 = forms.CharField(max_length=200, required=False, label="Feature 3")
    feature_4 = forms.CharField(max_length=200, required=False, label="Feature 4")
    feature_5 = forms.CharField(max_length=200, required=False, label="Feature 5")
    
    # Specifications as textarea with Key: Value format
    specifications_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'cols': 60}),
        required=False,
        label="Specifications",
        help_text='Enter each specification on a new line in format: Key: Value<br>Example:<br>Weight: 500g<br>Color: Blue<br>Material: Plastic'
    )
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load existing features
        if self.instance and self.instance.features:
            features_list = self.instance.features
            for i, feature in enumerate(features_list[:5], 1):
                field_name = f'feature_{i}'
                if field_name in self.fields:
                    self.initial[field_name] = feature
        
        # Load existing specifications
        if self.instance and self.instance.specifications:
            specs_dict = self.instance.specifications
            specs_text = '\n'.join([f'{k}: {v}' for k, v in specs_dict.items()])
            self.initial['specifications_text'] = specs_text
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Convert features to list
        features = []
        for i in range(1, 6):
            feature = cleaned_data.get(f'feature_{i}', '').strip()
            if feature:
                features.append(feature)
        cleaned_data['features'] = features
        
        # Convert specifications text to dict
        specs_text = cleaned_data.get('specifications_text', '').strip()
        specifications = {}
        if specs_text:
            for line in specs_text.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    specifications[key.strip()] = value.strip()
        cleaned_data['specifications'] = specifications
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.features = self.cleaned_data['features']
        instance.specifications = self.cleaned_data['specifications']
        if commit:
            instance.save()
        return instance