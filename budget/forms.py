from django import forms
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field
from crispy_forms.bootstrap import StrictButton

from .models import Budget, Category


class BudgetAddForm(forms.Form):
    category = forms.ModelChoiceField(
            label='Category',
            queryset=None,
            empty_label='Select',
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
            max_length=50,
            required=False,
    )

    def __init__(self, *args, **kwargs):
        super(BudgetAddForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = self.initial['categories']
        self.fields['category'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_class = 'form-crispy'
        self.helper.form_method = 'post'
        self.helper.form_action = 'wilbur:add-budget'
        self.helper.attrs = {'next': '/budgets/'}
        self.helper.layout = Layout(
                'category',
                HTML("""
                <script>
                    $(document).ready(function() {
                        $('select').niceSelect();
                    });
                </script>
                """),
                'amount',
                'description',
                StrictButton('Submit', type='submit', css_id='form-submit', css_class="button-submit"),
                HTML("""<a href="{% url 'wilbur:budgets' %}" class="button-cancel" role="button">Cancel</a>"""),
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'budget/js/niceselect.js' %}"></script>
                <script src="{% static 'budget/js/validator.js' %}"></script>
                """)
        )


class BudgetEditForm(forms.Form):
    category = forms.ModelChoiceField(
            label='Category',
            queryset=None,
            empty_label='Select',
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
            max_length=50,
            required=False,
    )

    def __init__(self, *args, **kwargs):
        super(BudgetEditForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = self.initial['categories']
        self.fields['category'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_class = 'form-crispy'
        self.helper.form_method = 'post'
        self.helper.form_action = 'wilbur:edit-budget'
        self.helper.attrs = {'next': '/budgets/'}
        self.helper.layout = Layout(
                'category',
                HTML("""
                <script>
                    $(document).ready(function() {
                        $('select').niceSelect();
                    });
                </script>
                """),
                'amount',
                'description',
                StrictButton('Submit', type='submit', css_id='form-submit', css_class="button-submit"),
                HTML("""<a href="{% url 'wilbur:budgets' %}" class="button-cancel" role="button">Cancel</a>"""),
                HTML("""
                <a href="{% url 'wilbur:delete-budget' budget_id %}" id="confirm" class="button-delete pull-right"
                 data-alt-text="Are you sure?" data-original-text="Delete" role="button">Delete</a>
                """),
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'budget/js/niceselect.js' %}"></script>
                <script src="{% static 'budget/js/validator.js' %}"></script>
                <script src="{% static 'budget/js/confirm.js' %}"></script>
                """)
        )


class TransactionAddForm(forms.Form):
    budget = forms.ModelChoiceField(
            label='Budget',
            queryset=None,
            empty_label='Select',
            required=True,
    )
    description = forms.CharField(
            label='Description',
            max_length=75,
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
            label='Transaction Date',
            required=True,
    )

    def __init__(self, *args, **kwargs):
        super(TransactionAddForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.initial['user'])
        self.fields['budget'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_class = 'form-crispy'
        self.helper.form_method = 'post'
        self.helper.form_action = 'wilbur:add-transaction'
        self.helper.attrs = {'next': '/transactions/'}
        self.helper.layout = Layout(
                'budget',
                HTML("""
                <script>
                    $(document).ready(function() {
                        $('select').niceSelect();
                    });
                </script>
                """),
                'amount',
                'transaction_date',
                HTML("""
                <script>
                    $("#id_transaction_date").minical({
                        initialize_with_date: false,
                    });
                </script>
                """),
                'description',
                StrictButton('Submit', type='submit', css_id='form-submit', css_class="button-submit"),
                HTML("""
                <a href="{% url 'wilbur:transactions' %}" class="button-cancel" role="button">Cancel</a>"""),
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'budget/js/niceselect.js' %}"></script>
                <script src="{% static 'budget/js/validator.js' %}"></script>
                """)
        )


class TransactionEditForm(forms.Form):
    budget = forms.ModelChoiceField(
            label='Budget',
            queryset=None,
            empty_label='Select',
            required=True,
    )
    description = forms.CharField(
            label='Description',
            max_length=75,
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
            label='Transaction Date',
            required=True,
    )

    def __init__(self, *args, **kwargs):
        super(TransactionEditForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.initial['user'])
        self.fields['budget'].to_field_name = 'id'

        self.helper = FormHelper()
        self.helper.form_id = 'form-grab'
        self.helper.form_class = 'form-crispy'
        self.helper.form_method = 'post'
        self.helper.form_action = 'wilbur:edit-transaction'
        self.helper.attrs = {'next': '/transactions/'}
        self.helper.layout = Layout(
                'budget',
                HTML("""
                <script>
                    $(document).ready(function() {
                        $('select').niceSelect();
                    });
                </script>
                """),
                'amount',
                'transaction_date',
                HTML("""
                <script>
                    $("#id_transaction_date").minical();
                </script>
                """),
                'description',
                StrictButton('Submit', type='submit', css_id='form-submit', css_class="button-submit"),
                HTML("""
                <a href="{% url 'wilbur:transactions' %}" class="button-cancel" role="button">Cancel</a>"""),
                HTML("""
                <a href="{% url 'wilbur:delete-transaction' transaction_id %}" id="confirm" class="button-delete pull-right"
                 data-alt-text="Are you sure?" data-original-text="Delete" role="button">Delete</a>
                """),
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'budget/js/niceselect.js' %}"></script>
                <script src="{% static 'budget/js/validator.js' %}"></script>
                <script src="{% static 'budget/js/confirm.js' %}"></script>
                """)
        )
