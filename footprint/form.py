from django import forms
from .models import Product_details

class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product_details
        fields = ['product_name', 'quantity', 'product_category']
