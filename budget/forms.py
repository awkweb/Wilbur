from django import forms
from django.forms.widgets import DateTimeInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from crispy_forms.bootstrap import StrictButton, PrependedAppendedText

from .models import Item, ItemType


class BudgetForm(forms.Form):
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True
    )

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                PrependedAppendedText('amount', '$'),
                StrictButton('Submit', css_class='btn-default', type='submit'),
                HTML("""<a class="btn btn-link" href="{% url 'budget:budget' %}" role="button">Cancel</a>""")
        )


class ItemAddForm(forms.Form):
    type = forms.ModelChoiceField(
            label='Type',
            queryset=ItemType.objects.all(),
            empty_label='',
            required=True,
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True,
    )
    description = forms.CharField(
            label='Description',
            max_length=100,
            required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ItemAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                'type',
                PrependedAppendedText('amount', '$'),
                'description',
                StrictButton('Submit', css_class='btn-default', type='submit'),
                HTML("""<a class="btn btn-link" href="{% url 'budget:budget' %}" role="button">Cancel</a>""")
        )


class ItemEditForm(forms.Form):
    type = forms.ModelChoiceField(
            label='Type',
            queryset=ItemType.objects.all(),
            empty_label='',
            required=True,
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True,
    )
    description = forms.CharField(
            label='Description',
            max_length=100,
            required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ItemEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                'type',
                PrependedAppendedText('amount', '$'),
                'description',
                StrictButton('Submit', css_class='btn-default', type='submit'),
                HTML("""<a class="btn btn-link" href="{% url 'budget:budget' %}" role="button">Cancel</a>"""),
                HTML("""<a class="btn btn-danger pull-right" href="{% url 'budget:delete-item' item_id %}" role="button">Delete</a>""")
        )


class TransactionAddForm(forms.Form):
    item = forms.ModelChoiceField(
            label='Budget item',
            queryset=None,
            empty_label='',
            required=True,
    )
    description = forms.CharField(
            label='Description',
            max_length=100,
            required=False,
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True,
    )
    transaction_date = forms.DateTimeField(
            label='Transaction date',
            widget=DateTimeInput(attrs={'type': 'datetime'}),
            required=True,
    )

    def __init__(self, *args, **kwargs):
        super(TransactionAddForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(budget=self.initial['budget'])
        self.fields['item'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_id = 'transaction-add'
        self.helper.form_method = 'post'
        self.helper.form_action = 'budget:add-transaction'
        self.helper.attrs = {'next': '/budget/transactions/'}
        self.helper.layout = Layout(
                'item',
                'description',
                PrependedAppendedText('amount', '$'),
                'transaction_date',
                StrictButton('Submit', type='submit', css_class='btn-default', css_id='transaction-add-submit'),
                HTML("""<a class="btn btn-link" href="{% url 'budget:transactions' %}" role="button">Cancel</a>""")
        )


class TransactionEditForm(forms.Form):
    item = forms.ModelChoiceField(
            label='Budget item',
            queryset=None,
            empty_label='',
            required=True,
    )
    description = forms.CharField(
            label='Description',
            max_length=100,
            required=False,
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True,
    )
    transaction_date = forms.DateTimeField(
            label='Transaction date',
            widget=DateTimeInput(attrs={'type': 'datetime'}),
            required=True,
    )

    def __init__(self, *args, **kwargs):
        super(TransactionEditForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(budget=self.initial['budget'])
        self.fields['item'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                'item',
                'description',
                PrependedAppendedText('amount', '$'),
                'transaction_date',
                StrictButton('Submit', css_class='btn-default', type='submit'),
                HTML("""<a class="btn btn-link" href="{% url 'budget:transactions' %}" role="button">Cancel</a>"""),
                HTML("""<a class="btn btn-danger pull-right" href="{% url 'budget:delete-transaction' transaction_id %}" role="button">Delete</a>""")
        )