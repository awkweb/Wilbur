from django import forms
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from crispy_forms.bootstrap import StrictButton, PrependedAppendedText

from .models import Budget, Category


class BudgetAddForm(forms.Form):
    category = forms.ModelChoiceField(
            label='Category',
            queryset=Category.objects.all(),
            empty_label='',
            required=True,
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True
    )
    description = forms.CharField(
            label='Description',
            max_length=100,
            required=False,
    )

    def __init__(self, *args, **kwargs):
        super(BudgetAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_method = 'post'
        self.helper.form_action = 'budget:add-budget'
        self.helper.attrs = {'next': '/budget/budgets/'}
        self.helper.layout = Layout(
                'category',
                PrependedAppendedText('amount', '$'),
                'description',
                StrictButton('Submit', type='submit', css_class='btn-default', css_id='form-submit'),
                HTML("""<a class="btn btn-link" href="{% url 'budget:budgets' %}" role="button">Cancel</a>""")
        )


class BudgetEditForm(forms.Form):
    category = forms.ModelChoiceField(
            label='Category',
            queryset=Category.objects.all(),
            empty_label='',
            required=True,
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True
    )
    description = forms.CharField(
            label='Description',
            max_length=100,
            required=False,
    )

    def __init__(self, *args, **kwargs):
        super(BudgetEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_method = 'post'
        self.helper.form_action = 'budget:edit-budget'
        self.helper.attrs = {'next': '/budget/budgets/'}
        self.helper.layout = Layout(
                'category',
                PrependedAppendedText('amount', '$'),
                'description',
                StrictButton('Submit', type='submit', css_class='btn-default', css_id='form-submit'),
                HTML("""<a href="{% url 'budget:budgets' %}" role="button">Cancel</a>"""),
                HTML("""<a href="{% url 'budget:delete-budget' budget_id %}" role="button">Delete</a>""")
        )


class TransactionAddForm(forms.Form):
    budget = forms.ModelChoiceField(
            label='Budget',
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
    transaction_date = forms.DateField(
            label='Transaction date',
            widget=DateInput(attrs={'type': 'date'}),
            required=True,
    )

    def __init__(self, *args, **kwargs):
        super(TransactionAddForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.initial['user'])
        self.fields['budget'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_method = 'post'
        self.helper.form_action = 'budget:add-transaction'
        self.helper.attrs = {'next': '/budget/transactions/'}
        self.helper.layout = Layout(
                'budget',
                'description',
                PrependedAppendedText('amount', '$'),
                'transaction_date',
                StrictButton('Submit', type='submit', css_class='btn-default', css_id='form-submit'),
                HTML("""<a class="btn btn-link" href="{% url 'budget:transactions' %}" role="button">Cancel</a>""")
        )


class TransactionEditForm(forms.Form):
    budget = forms.ModelChoiceField(
            label='Budget',
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
    transaction_date = forms.DateField(
            label='Transaction date',
            widget=DateInput(attrs={'type': 'date'}),
            required=True,
    )

    def __init__(self, *args, **kwargs):
        super(TransactionEditForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.initial['user'])
        self.fields['budget'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_method = 'post'
        self.helper.form_action = 'budget:edit-transaction'
        self.helper.attrs = {'next': '/budget/transactions/'}
        self.helper.layout = Layout(
                'budget',
                'description',
                PrependedAppendedText('amount', '$'),
                'transaction_date',
                StrictButton('Submit', type='submit', css_id='form-submit'),
                HTML("""<a href="{% url 'budget:transactions' %}" role="button">Cancel</a>"""),
                HTML("""<a href="{% url 'budget:delete-transaction' transaction_id %}" role="button">Delete</a>""")
        )