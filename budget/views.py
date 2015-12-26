from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.core.context_processors import csrf

from jsonview.decorators import json_view
from pytz import timezone
from crispy_forms.utils import render_crispy_form

from .models import Budget, Transaction
from .forms import TransactionAddForm, TransactionEditForm, BudgetAddForm, BudgetEditForm


class BudgetsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budgets = get_budgets_for_user(user)

        today = now()
        current_month = today.month
        current_year = today.year
        budget_list = []
        for budget in budgets:
            amount_spent = budget.get_sum_transactions_for_month_and_year(current_month, current_year)
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

        return render(request, 'budget/budgets.html', {
            'title': 'Budgets',
            'budgets': budgets,
            'budget_list': budget_list,
        })


@login_required(login_url='/login/', redirect_field_name='next')
@json_view
def add_budget(request):
    if request.method == 'POST':
        form = BudgetAddForm(request.POST)
        if form.is_valid():
            user = get_user_in_session(request.session)
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            creation_date = now().date()
            budget = Budget(user=user, category=category, amount=amount, description=description, creation_date=creation_date)
            budget.save()
            return {
                'success': True,
            }
        request_context = RequestContext(request)
        form_html = render_crispy_form(form, context=request_context)
        return {
            'success': False,
            'form_html': form_html,
        }
    else:
        form = BudgetAddForm()
        form.helper.form_action = reverse('budget:add-budget')
        return render(request, 'base_form.html', {
            'title': 'Add Budget',
            'form': form,
        })


@login_required(login_url='/login/', redirect_field_name='next')
@json_view
def edit_budget(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    data = {
        'category': budget.category.id,
        'amount': budget.amount,
        'description': budget.description,
    }
    if request.method == 'POST':
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
            return {
                'success': True,
            }
        request_context = RequestContext(request)
        form_html = render_crispy_form(form, context=request_context)
        return {
            'success': False,
            'form_html': form_html,
            'budget_id': budget.id,
        }
    else:
        form = BudgetEditForm(data)
        form.helper.form_action = reverse('budget:edit-budget', kwargs={'budget_id': budget.id})
        return render(request, 'base_form.html', {
            'title': 'Edit Budget',
            'form': form,
            'budget_id': budget.id,
        })


@login_required(login_url='/login/', redirect_field_name='next')
def delete_budget(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    budget.delete()
    return redirect('budget:budgets')


class TransactionsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budgets = get_budgets_for_user(user)
        today = now()
        current_month = today.month
        current_year = today.year
        transaction_list = []
        for budget in budgets:
            t_list = budget.get_transactions_for_month_and_year(current_month, current_year)
            transaction_list.extend(t_list)
        transaction_list = sorted(transaction_list, reverse=True, key=lambda t: t.transaction_date)
        transactions = get_paginator_for_list(request, transaction_list, 10)
        return render_to_response('budget/transactions.html', {
            'title': 'Transactions',
            'transactions': transactions,
        })


@login_required(login_url='/login/', redirect_field_name='next')
@json_view
def add_transaction(request):
    user = get_user_in_session(request.session)
    data = {'user': user}

    if request.method == 'POST':
        form = TransactionAddForm(request.POST, initial=data)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            transaction_date = form.cleaned_data['transaction_date']
            creation_date = now().date()
            transaction = Transaction(
                    budget=budget,
                    description=description,
                    amount=amount,
                    transaction_date=transaction_date,
                    creation_date=creation_date
            )
            transaction.save()
            return {
                'success': True,
            }
        context = {}
        context.update(csrf(request))
        form_html = render_crispy_form(form, context=context)
        return {
            'success': False,
            'form_html': form_html,
        }
    else:
        form = TransactionAddForm(initial=data)
        return render(request, 'base_form.html', {
            'title': 'Add Transaction',
            'form': form,
        })


@login_required(login_url='/login/', redirect_field_name='next')
@json_view
def edit_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    user = get_user_in_session(request.session)
    data = {
        'budget': transaction.budget.id,
        'description': transaction.description,
        'amount': transaction.amount,
        'transaction_date': transaction.transaction_date,
        'user': user
    }
    if request.method == 'POST':
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
            return {
                'success': True,
            }
        request_context = RequestContext(request)
        form_html = render_crispy_form(form, context=request_context)
        return {
            'success': False,
            'form_html': form_html,
            'transaction_id': transaction.id,
        }
    else:
        form = TransactionEditForm(data, initial={'user': user})
        form.helper.form_action = reverse('budget:edit-transaction', kwargs={'transaction_id': transaction.id})
        return render(request, 'base_form.html', {
            'title': 'Edit Transaction',
            'form': form,
            'transaction_id': transaction.id,
        })


@login_required(login_url='/login/', redirect_field_name='next')
def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.delete()
    return redirect('budget:transactions')


def get_user_in_session(session):
    user_id = session['_auth_user_id']
    user = User.objects.get(pk=user_id)
    return user


def get_budgets_for_user(user):
    budgets = None
    try:
        budgets = Budget.objects.filter(user=user)
    finally:
        if budgets is None:
            return None
        else:
            return budgets


def get_paginator_for_list(request, array_list, max_per_page):
    paginator = Paginator(array_list, max_per_page)

    page = request.GET.get('page')
    try:
        array = paginator.page(page)
    except PageNotAnInteger:
        array = paginator.page(1)
    except EmptyPage:
        array = paginator.page(paginator.num_pages)
    return array
