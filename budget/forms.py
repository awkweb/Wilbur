from django import forms
from django.forms.widgets import DateTimeInput

from .models import Item


class AddTransactionForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    item = forms.ModelChoiceField(queryset=Item.objects.all())
    name = forms.CharField(label='Name', max_length=100)
    amount = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    transaction_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime'}))

