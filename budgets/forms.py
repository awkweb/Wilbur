from django import forms

from budgets.models import Budget


class BudgetAddForm(forms.Form):
    category = forms.ModelChoiceField(
            label='Category',
            queryset=None,
            empty_label='Select category',
            required=True,
            widget=forms.Select(attrs={'class': 'form-input', 'required': 'required', 'autofocus': 'autofocus'}),
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-input', 'required': 'required', 'placeholder': '99.50'}),
    )
    description = forms.CharField(
            label='Description',
            max_length=50,
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-input', 'required': 'required',
                                          'placeholder': 'A short clever description', 'data_coffee': "description"}),
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
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'js/niceselect.js' %}"></script>
                <script src="{% static 'js/coffeecounter.js' %}"></script>
                """),
                'category',
                HTML("""
                <script>
                    $(document).ready(function() {
                        $('select').niceSelect();
                    });
                </script>
                """),
                Field('amount', placeholder='100.00'),
                Field('description', placeholder='A short, clever description'),
                HTML("""
                <script>
                    $("#id_description").coffeeCounter();
                </script>
                """),
                StrictButton('Save', type='submit', css_id='form-submit', css_class="button-submit"),
                HTML("""<a href="{% url 'wilbur:budgets' %}" class="button-cancel" role="button">Cancel</a>"""),
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'js/validator.js' %}"></script>
                """)
        )


class BudgetEditForm(forms.Form):
    category = forms.ModelChoiceField(
            label='Category',
            queryset=None,
            empty_label='Select category',
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
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'js/niceselect.js' %}"></script>
                <script src="{% static 'js/coffeecounter.js' %}"></script>
                """),
                'category',
                HTML("""
                <script>
                    $(document).ready(function() {
                        $('select').niceSelect();
                    });
                </script>
                """),
                Field('amount', placeholder='100.00'),
                Field('description', placeholder='A short, clever description'),
                HTML("""
                <script>
                    $("#id_description").coffeeCounter();
                </script>
                """),
                StrictButton('Save', type='submit', css_id='form-submit', css_class="button-submit"),
                HTML("""<a href="{% url 'wilbur:budgets' %}" class="button-cancel" role="button">Cancel</a>"""),
                HTML("""
                <a href="{% url 'wilbur:delete-budget' budget_id %}" id="confirm" class="button-delete pull-right"
                 data-alt-text="Yes, I am sure." data-original-text="Delete" role="button">Delete</a>
                """),
                HTML("""
                {% load staticfiles %}
                <script src="{% static 'js/confirm.js' %}"></script>
                <script src="{% static 'js/validator.js' %}"></script>
                """)
        )


class TransactionAddForm(forms.Form):
    budget = forms.ModelChoiceField(
            label='Budget',
            queryset=None,
            empty_label='Select budget',
            required=True,
            widget=forms.Select(attrs={'class': 'form-input', 'required': 'required', 'autofocus': 'autofocus'}),
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-input', 'required': 'required', 'placeholder': '7.99'}),
    )
    transaction_date = forms.DateField(
            label='Transaction Date',
            required=True,
            widget=forms.DateInput(attrs={'class': 'form-input', 'required': 'required', 'placeholder': '10/15/1952'}),
    )
    description = forms.CharField(
            label='Description',
            max_length=75,
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-input', 'required': 'required',
                                          'placeholder': 'Netflix – and chill?', 'data_coffee': "description"}),
    )

    def __init__(self, *args, **kwargs):
        super(TransactionAddForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.initial['user']).order_by('category__name')
        self.fields['budget'].to_field_name = 'id'


class TransactionEditForm(forms.Form):
    budget = forms.ModelChoiceField(
            label='Budget',
            queryset=None,
            empty_label='Select budget',
            required=True,
            widget=forms.Select(attrs={'class': 'form-input', 'required': 'required', 'autofocus': 'autofocus'}),
    )
    amount = forms.DecimalField(
            label='Amount',
            min_value=0,
            max_digits=10,
            decimal_places=2,
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-input', 'required': 'required', 'placeholder': '7.99'}),
    )
    transaction_date = forms.DateField(
            label='Transaction Date',
            required=True,
            widget=forms.DateInput(attrs={'class': 'form-input', 'required': 'required', 'placeholder': '10/15/1952'}),
    )
    description = forms.CharField(
            label='Description',
            max_length=75,
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-input', 'required': 'required',
                                          'placeholder': 'Netflix – and chill?', 'data_coffee': "description"}),
    )

    def __init__(self, *args, **kwargs):
        super(TransactionEditForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.initial['user']).order_by('category__name')
        self.fields['budget'].to_field_name = 'id'
