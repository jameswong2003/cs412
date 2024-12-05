from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'picture_url', 'description', 'price']

# shop/forms.py

from .models import Business

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name']