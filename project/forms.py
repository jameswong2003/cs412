from django import forms
from .models import Product, Business

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'picture_url', 'description', 'price']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description']
