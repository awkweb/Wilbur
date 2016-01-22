from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.generic.base import TemplateView

from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form

from cuser.forms import UserCreationForm
from budgets.forms import BudgetAddForm, BudgetEditForm, TransactionAddForm, TransactionEditForm
from budgets.utils import *


class OverviewView(TemplateView):

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)

        if user is None:
            return render(request, 'overview/landing.html', {
                'title': 'Track your budgets better',
            })
        else:
            budgets = get_budgets_for_user(user)

            if budgets:
                today = now()

                request.session['selectdate_value'] = "%s%s" % (today.month, today.year)
                request.session['month'] = today.month
                request.session['year'] = today.year

                budget_list = []
                transaction_list = []
                remaining = 0
                total = 0
                for budget in budgets:
                    amount_spent = get_sum_transactions_for_budget_with_month_and_year(budget, today.month, today.year)
                    amount_left = budget.amount - amount_spent
                    amount_percent = amount_spent / budget.amount * 100
                    data = {
                        'id': budget.id,
                        'name': budget.category.name.title(),
                        'amount': budget.amount,
                        'amount_spent': amount_spent,
                        'amount_left': amount_left,
                        'description': budget.description,
                        'percent': amount_percent
                    }
                    remaining += amount_left
                    total += budget.amount
                    budget_list.append(data)
                    t_list = get_transactions_for_budget_with_month_and_year(budget, today.month, today.year)
                    transaction_list.extend(t_list)

                budget_list = sorted(budget_list, key=lambda b: b['percent'], reverse=True)[:5]
                transaction_list = sorted(transaction_list, reverse=True, key=lambda t: t.transaction_date)[:5] # ToDo model level sorting
                remaining_percent = remaining / total * 100

                return render(request, 'overview/overview.html', {
                    'title': 'Overview',
                    'user': user,
                    'total': total,
                    'remaining': remaining,
                    'remaining_percent': remaining_percent,
                    'budget_list': budget_list,
                    'transaction_list': transaction_list,
                })
            else:
                return render(request, 'overview/overview.html', {
                    'title': 'Overview',
                    'user': user,
                })


class BudgetsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budgets = get_budgets_for_user(user)

        today = now()
        month = request.session.get('month', today.month)
        year = request.session.get('year', today.year)
        selectdate_value = request.session.get('selectdate_value', "%s%s" % (today.month, today.year))
        months = Transaction.objects.filter(budget__user=user).dates('transaction_date', 'month', 'DESC')
        if months.count() == 0:
            month = today.month
            year = today.year
            selectdate_value = "%s%s" % (today.month, today.year)
        elif months.count() == 1:
            selectdate = months.first()
            month = selectdate.month
            year = selectdate.year
            selectdate_value = "%s%s" % (selectdate.month, selectdate.year)

        budget_list = []
        remaining = 0
        total = 0
        for budget in budgets:
            amount_spent = get_sum_transactions_for_budget_with_month_and_year(budget, month, year)
            amount_left = budget.amount - amount_spent
            amount_percent = amount_spent / budget.amount * 100
            data = {
                'id': budget.id,
                'name': budget.category.name.title(),
                'amount': budget.amount,
                'amount_spent': amount_spent,
                'amount_left': amount_left,
                'description': budget.description,
                'percent': amount_percent
            }
            remaining += amount_left
            total += budget.amount
            budget_list.append(data)
        budget_overall = {
            'name': date(int(year), month=int(month), day=1),
            'amount': total,
            'amount_spent': total - remaining,
            'amount_left': remaining,
            'percent': (total - remaining) / total * 100 if total > 0 else 0
        }

        return render(request, 'budgets/budgets.html', {
            'title': 'Budgets',
            'budget': budget_overall,
            'budget_list': budget_list,
            'selectdate_value': selectdate_value,
            'months': months,
        })

    @json_view
    def post(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budgets = get_budgets_for_user(user)

        data = request.POST
        selectdate_value = data['selectdate_value']
        month = data['month']
        year = data['year']
        request.session['selectdate_value'] = selectdate_value
        request.session['month'] = month
        request.session['year'] = year

        budget_list = []
        remaining = 0
        total = 0
        for budget in budgets:
            amount_spent = get_sum_transactions_for_budget_with_month_and_year(budget, month, year)
            amount_left = budget.amount - amount_spent
            amount_percent = amount_spent / budget.amount * 100
            data = {
                'id': budget.id,
                'name': budget.category.name,
                'amount': budget.amount,
                'amount_spent': amount_spent,
                'amount_left': amount_left,
                'description': budget.description,
                'percent': amount_percent
            }
            remaining += amount_left
            total += budget.amount
            budget_list.append(data)

        budget_overall = {
            'name': date(int(year), month=int(month), day=1),
            'amount': total,
            'amount_spent': total - remaining,
            'amount_left': remaining,
            'percent': (total - remaining) / total * 100
        }
        html = render(request, 'budgets/budgets_progress.html', {
            'budget': budget_overall,
            'budget_list': budget_list,
        })
        html = html.content.decode("utf-8")
        return {
            'success': True,
            'html': html,
        }


class BudgetsAddView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        categories = get_unused_categories_for_user(user)
        data = {'categories': categories}
        form = BudgetAddForm(initial=data)
        form.helper.form_action = reverse('wilbur:add-budget')
        return render(request, 'base_form.html', {
            'title': 'Add Budget',
            'form': form,
        })

    @json_view
    def post(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        categories = get_unused_categories_for_user(user)
        data = {'categories': categories}
        form = BudgetAddForm(request.POST, initial=data)
        if form.is_valid():
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            budget = Budget(user=user, category=category, amount=amount, description=description)
            budget.save()
            messages.success(request, 'Budget added')
            return {
                'success': True,
            }
        form_html = render_crispy_form(form)
        return {
            'success': False,
            'form_html': form_html,
        }


class BudgetsEditView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        budget_id = kwargs['budget_id']
        budget = Budget.objects.get(pk=budget_id)
        user = get_user_in_session(request.session)
        if budget.user == user:
            categories = get_unused_categories_for_user(user, budget.category)
            data = {
                'category': budget.category.id,
                'amount': budget.amount,
                'description': budget.description,
                'categories': categories,
            }
            form = BudgetEditForm(data, initial={'categories': categories})
            form.helper.form_action = reverse('wilbur:edit-budget', kwargs={'budget_id': budget_id})
            return render(request, 'base_form.html', {
                'title': 'Edit Budget',
                'form': form,
                'budget_id': budget.id,
            })
        else:
            raise Http404("Budget does not exist")

    @json_view
    def post(self, request, *args, **kwargs):
        budget_id = kwargs['budget_id']
        budget = Budget.objects.get(pk=budget_id)
        user = get_user_in_session(request.session)
        categories = get_unused_categories_for_user(user, budget.category)
        data = {
            'category': budget.category.id,
            'amount': budget.amount,
            'description': budget.description,
            'categories': categories,
        }
        form = BudgetEditForm(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    cleaned_data = form.cleaned_data[field]
                    if field == 'category':
                        budget.category = cleaned_data
                    elif field == 'amount':
                        budget.amount = cleaned_data
                    elif field == 'description':
                        budget.description = cleaned_data
                budget.save()
            messages.success(request, 'Budget updated')
            return {'success': True}
        context = {'budget_id': budget_id}
        form.helper.form_action = reverse('wilbur:edit-budget', kwargs={'budget_id': budget_id})
        form_html = render_crispy_form(form, context=context)
        return {
            'success': False,
            'form_html': form_html,
        }


@login_required(login_url='/login/', redirect_field_name='next')
def delete_budget(request, budget_id):
    budget = Budget.objects.get(pk=budget_id) # ToDo check if budget belongs to user
    budget.delete()
    messages.success(request, 'Budget deleted')
    return redirect('wilbur:budgets')


class TransactionsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)

        today = now()
        month = request.session.get('month', today.month)
        year = request.session.get('year', today.year)
        selectdate_value = request.session.get('selectdate_value', "%s%s" % (today.month, today.year))
        months = Transaction.objects.filter(budget__user=user).dates('transaction_date', 'month', 'DESC')
        if months.count() == 0:
            month = today.month
            year = today.year
            selectdate_value = "%s%s" % (today.month, today.year)
        elif months.count() == 1:
            selectdate = months.first()
            month = selectdate.month
            year = selectdate.year
            selectdate_value = "%s%s" % (selectdate.month, selectdate.year)
        filter_value = kwargs.get('budget_id', '-1')

        if filter_value == '-1':
            transaction_list = get_transactions_with_month_and_year(user, month, year)
        else:
            budget = Budget.objects.get(pk=filter_value)
            if budget.user != user:
                raise Http404("Budget does not exist")
            transaction_list = get_transactions_for_budget_with_month_and_year(filter_value, month, year)
        transactions = get_paginator_for_list(request, transaction_list, 10)

        budget_list = []
        budgets = get_budgets_for_user(user)
        for budget in budgets:
            b = {
                'id': budget.id,
                'name': budget.category.name,
            }
            budget_list.append(b)
        return render(request, 'transactions/transactions.html', {
            'title': 'Transactions',
            'hasBudget': budgets.count() == 0,
            'transactions': transactions,
            'selectdate_value': selectdate_value,
            'months': months,
            'filter_value': filter_value,
            'budget_list': budget_list,
        })

    @json_view
    def post(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)

        data = request.POST
        selectdate_value = data['selectdate_value']
        request.session['selectdate_value'] = selectdate_value
        month = data['month']
        year = data['year']
        request.session['month'] = month
        request.session['year'] = year
        filter_value = kwargs.get('budget_id', '-1')

        if filter_value == '-1':
            transaction_list = get_transactions_with_month_and_year(user, month, year)
        else:
            budget = Budget.objects.get(pk=filter_value)
            if budget.user != user:
                raise Http404("Budget does not exist")
            transaction_list = get_transactions_for_budget_with_month_and_year(filter_value, month, year)
        transactions = get_paginator_for_list(request, transaction_list, 10)

        html = render(request, 'transactions/transactions_table.html', {
            'transactions': transactions,
        })
        html = html.content.decode("utf-8")
        return {
            'success': True,
            'html': html,
        }


class TransactionsAddView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        data = {'user': user}
        form = TransactionAddForm(initial=data)
        return render(request, 'base_form.html', {
            'title': 'Add Transaction',
            'form': form,
        })

    @json_view
    def post(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        data = {'user': user}
        form = TransactionAddForm(request.POST, initial=data)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            transaction_date = form.cleaned_data['transaction_date']
            transaction = Transaction(
                    budget=budget,
                    description=description,
                    amount=amount,
                    transaction_date=transaction_date
            )
            transaction.save()
            messages.success(request, 'Transaction added')
            return {'success': True}
        form_html = render_crispy_form(form)
        return {
            'success': False,
            'form_html': form_html,
        }


class TransactionsEditView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        transaction_id = kwargs['transaction_id']
        transaction = Transaction.objects.get(pk=transaction_id)
        user = get_user_in_session(request.session)
        if transaction.budget.user == user:
            data = {
                'budget': transaction.budget.id,
                'description': transaction.description,
                'amount': transaction.amount,
                'transaction_date': transaction.transaction_date,
                'user': user,
            }
            form = TransactionEditForm(data, initial={'user': user}, label_suffix='')
            form.helper.form_action = reverse('wilbur:edit-transaction', kwargs={'transaction_id': transaction_id})
            return render(request, 'base_form.html', {
                'title': 'Edit Transaction',
                'form': form,
                'transaction_id': transaction_id,
            })
        else:
            raise Http404("Transaction does not exist")

    @json_view
    def post(self, request, *args, **kwargs):
        transaction_id = kwargs.pop('transaction_id', None)
        transaction = Transaction.objects.get(pk=transaction_id)
        user = get_user_in_session(request.session)
        data = {
            'budget': transaction.budget.id,
            'description': transaction.description,
            'amount': transaction.amount,
            'transaction_date': transaction.transaction_date,
            'user': user,
        }
        form = TransactionEditForm(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    cleaned_data = form.cleaned_data[field]
                    if field == 'budget':
                        transaction.budget = cleaned_data
                    elif field == 'description':
                        transaction.description = cleaned_data
                    elif field == 'amount':
                        transaction.amount = cleaned_data
                    elif field == 'transaction_date':
                        transaction.transaction_date = cleaned_data
                transaction.save()
            messages.success(request, 'Transaction updated')
            return {'success': True}
        context = {'transaction_id': transaction_id}
        form.helper.form_action = reverse('wilbur:edit-transaction', kwargs={'transaction_id': transaction_id})
        form_html = render_crispy_form(form, context=context)
        return {
            'success': False,
            'form_html': form_html,
            'transaction_id': transaction.id,
        }


@login_required(login_url='/login/', redirect_field_name='next')
def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.delete()
    messages.success(request, 'Transaction deleted')
    return redirect('wilbur:transactions')


class SignUpView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm(label_suffix='')
        return render(request, 'base_form.html', {
            'title': 'Sign Up',
            'form': form,
        })

    @json_view
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            form.clean_password2()
            form.save()
            return {'success': True}
        form_html = render(request, 'base_form.html', {
            'form': form,
        })
        print(form_html)
        errors = form.error_messages
        print(errors)
        if errors:
            for field in form:
                for error in field.errors:
                    print(error)
        # return {
        #     'success': False,
        #     'form_html': form_html,
        #     'errors': errors,
        # }
        return render(request, 'base_form.html', {
            'title': 'Sign Up',
            'form': form,
        })
