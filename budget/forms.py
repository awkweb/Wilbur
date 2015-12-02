from django import forms
from django.forms.widgets import DateTimeInput

from .models import Item


class BudgetForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    amount = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)


class TransactionForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    item = forms.ModelChoiceField(queryset=Item.objects.all())
    description = forms.CharField(label='Description', max_length=100)
    amount = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    transaction_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime'}))

