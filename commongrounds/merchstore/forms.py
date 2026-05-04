from django import forms
from .models import Transaction, Product


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]


class CustomProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "product_type", "product_image",
            "description", "price", "stock", "status"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = ''
        self.fields['name'].help_text = '' 
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Product Name'
        })

        self.fields['product_type'].label = ''
        self.fields['product_type'].help_text = '' 
        self.fields['product_type'].widget.attrs.update({
            'placeholder': 'Category'
        })
        
        self.fields['description'].label = ''
        self.fields['description'].help_text = ''
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Product Description'
        })

        self.fields['price'].label = ''
        self.fields['price'].help_text = ''
        self.fields['price'].widget.attrs.update({
            'placeholder': 'Set Product Price'
        })

        self.fields['stock'].label = ''
        self.fields['stock'].help_text = ''
        self.fields['stock'].widget.attrs.update({
            'placeholder': 'Current Stock'
        })
