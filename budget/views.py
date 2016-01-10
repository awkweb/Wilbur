from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.generic.base import TemplateView

from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form

from .models import Transaction
from .forms import BudgetAddForm, BudgetEditForm, TransactionAddForm, TransactionEditForm
from .utils import *


class OverviewView(TemplateView):

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)

        if user is None:
            return render(request, 'budget/landing.html', {
                    'title': 'Track your monthly budgets',
                })
        else:
            budgets = get_budgets_for_user(user)

            if budgets:
                today = now()
                budget_list = []
                transaction_list = []
                remaining = 0
                total = 0
                for budget in budgets:
                    amount_spent = budget.get_sum_transactions_for_month_and_year(today.month, today.year)
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
                    if amount_percent != 100:
                        budget_list.append(data)
                    t_list = budget.get_transactions_for_month_and_year(today.month, today.year)
                    transaction_list.extend(t_list)

                budget_list = sorted(budget_list, key=lambda b: b['percent'], reverse=True)[:5]
                transaction_list = sorted(transaction_list, reverse=True, key=lambda t: t.transaction_date)[:5]
                remaining_percent = remaining / total * 100

                return render(request, 'budget/overview.html', {
                    'title': 'Overview',
                    'user': user,
                    'total': total,
                    'remaining': remaining,
                    'remaining_percent': remaining_percent,
                    'budget_list': budget_list,
                    'transaction_list': transaction_list,
                })
            else:
                return render(request, 'budget/overview.html', {
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
        select_value = request.session.get('select_value', "%s%s" % (today.month, today.year))
        months = Transaction.objects.filter(budget__user=user).dates('transaction_date', 'month', 'DESC')

        budget_list = []
        for budget in budgets:
            amount_spent = budget.get_sum_transactions_for_month_and_year(month, year)
            data = {
                'id': budget.id,
                'name': budget.category.name.title(),
                'amount': budget.amount,
                'amount_spent': amount_spent,
                'amount_left': budget.amount - amount_spent,
                'description': budget.description,
                'percent': amount_spent / budget.amount * 100
            }
            budget_list.append(data)

        return render(request, 'budget/budgets.html', {
            'title': 'Budgets',
            'budgets': budgets,
            'budget_list': budget_list,
            'select_value': select_value,
            'months': months,
        })

    @json_view
    def post(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budgets = get_budgets_for_user(user)

        data = request.POST
        select_value = data['select_value']
        month = data['month']
        year = data['year']
        request.session['select_value'] = select_value
        request.session['month'] = month
        request.session['year'] = year

        budget_list = []
        for budget in budgets:
            amount_spent = budget.get_sum_transactions_for_month_and_year(month, year)
            data = {
                'id': budget.id,
                'name': budget.category.name,
                'amount': budget.amount,
                'amount_spent': amount_spent,
                'amount_left': budget.amount - amount_spent,
                'description': budget.description,
                'percent': amount_spent / budget.amount * 100
            }
            budget_list.append(data)

        html = render(request, 'budget/includes/budgets_progress.html', {
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
    budget = Budget.objects.get(pk=budget_id)
    budget.delete()
    return redirect('wilbur:budgets')


class TransactionsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budgets = get_budgets_for_user(user)

        today = now()
        month = request.session.get('month', today.month)
        year = request.session.get('year', today.year)
        select_value = request.session.get('select_value', "%s%s" % (today.month, today.year))
        months = Transaction.objects.filter(budget__user=user).dates('transaction_date', 'month', 'DESC')

        transaction_list = []
        for budget in budgets:
            t_list = budget.get_transactions_for_month_and_year(month, year)
            transaction_list.extend(t_list)
        transaction_list = sorted(transaction_list, reverse=True, key=lambda t: t.transaction_date)
        transactions = get_paginator_for_list(request, transaction_list, 10)
        return render(request, 'budget/transactions.html', {
            'title': 'Transactions',
            'hasBudget': budgets.count() == 0,
            'transactions': transactions,
            'select_value': select_value,
            'months': months,
        })

    @json_view
    def post(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budgets = get_budgets_for_user(user)

        data = request.POST
        select_value = data['select_value']
        month = data['month']
        year = data['year']
        request.session['select_value'] = select_value
        request.session['month'] = month
        request.session['year'] = year

        transaction_list = []
        for budget in budgets:
            t_list = budget.get_transactions_for_month_and_year(month, year)
            transaction_list.extend(t_list)
        transaction_list = sorted(transaction_list, reverse=True, key=lambda t: t.transaction_date)
        transactions = get_paginator_for_list(request, transaction_list, 10)
        html = render(request, 'budget/includes/transactions_table.html', {
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
            return {'success': True}
        form_html = render_crispy_form(form)
        print(type(form_html))
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
            form = TransactionEditForm(data, initial={'user': user})
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
    return redirect('wilbur:transactions')

