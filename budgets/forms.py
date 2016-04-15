from django import forms

from budgets.models import Budget


class WilburForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(WilburForm, self).__init__(*args, **kwargs)


class BudgetForm(WilburForm):
    category = forms.ModelChoiceField(
            label='Category',
            queryset=None,
            empty_label='Select category',
            required=True,
            widget=forms.Select(attrs={'class': 'form-control', 'autofocus': ''}),
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=.009,
            max_digits=10,
            decimal_places=2,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '99.50'}),
    )
    description = forms.CharField(
            label='Description',
            max_length=50,
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A short, clever description',
                                          'data_coffee': "description"}),
    )

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = self.initial['categories']
        self.fields['category'].to_field_name = 'id'


class TransactionForm(WilburForm):
    budget = forms.ModelChoiceField(
            label='Budget',
            queryset=None,
            empty_label='Select budget',
            required=True,
            widget=forms.Select(attrs={'class': 'form-control', 'autofocus': ''}),
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=.009,
            max_digits=10,
            decimal_places=2,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '7.99'}),
    )
    transaction_date = forms.DateField(
            label='Transaction Date',
            required=True,
            widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '10/15/1952'}),
    )
    description = forms.CharField(
            label='Description',
            max_length=50,
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Netflix – and chill?',
                                          'data_coffee': "description"}),
    )

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.initial['user']).order_by('category__name')
        self.fields['budget'].to_field_name = 'id'
