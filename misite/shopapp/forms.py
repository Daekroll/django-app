from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "price", "discount",


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "address", "comment", "user", "products"


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()