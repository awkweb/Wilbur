from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.utils.timezone import now
from django.views.generic.base import TemplateView

from jsonview.decorators import json_view
from pytz import timezone
from crispy_forms.utils import render_crispy_form

from .models import Budget, Transaction, Item
from .forms import TransactionAddForm, TransactionEditForm, BudgetForm, ItemAddForm, ItemEditForm


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/budget/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budget = get_budget_for_user(user)

        if budget is not None:
            today = now()
            current_month = today.month
            current_year = today.year
            transactions = budget.get_transactions_for_month_and_year(current_month, current_year)[:5]
            total_spent = budget.get_sum_transactions_for_month_and_year(current_month, current_year)
            spent_percentage = total_spent / budget.amount * 100
            return render(request, 'budget/overview.html', {
                'title': 'Overview',
                'budget': budget,
                'transactions': transactions,
                'total_spent': total_spent,
                'spent_percentage': spent_percentage,
            })
        else:
            return render(request, 'budget/overview.html', {
                'title': 'Overview',
            })


class BudgetView(LoginRequiredMixin, TemplateView):
    login_url = '/budget/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budget = get_budget_for_user(user)

        if budget is not None:
            today = now()
            current_month = today.month
            current_year = today.year
            total_spent = budget.get_sum_transactions_for_month_and_year(current_month, current_year)
            spent_percentage = total_spent / budget.amount * 100
            items = budget.get_items()
            item_list = []
            for item in items:
                item_total_spent = item.get_sum_transactions_for_month_and_year(current_month, current_year)
                item_spent_percentage = item_total_spent / item.amount * 100
                item_list.append((item.id, item.type.name, item.amount, item_total_spent, item_spent_percentage))
            return render(request, 'budget/budget.html', {
                'title': 'Budget',
                'budget': budget,
                'total_spent': total_spent,
                'spent_percentage': spent_percentage,
                'item_list': item_list,
            })
        else:
            return render(request, 'budget/budget.html', {
                'title': 'Budget',
            })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            user = get_user_in_session(request.session)
            amount = form.cleaned_data['amount']
            creation_date = now()
            budget = Budget(user=user, amount=amount, creation_date=creation_date)
            budget.save()
            return redirect('budget:budget')
    else:
        form = BudgetForm()
        form.helper.form_action = reverse('budget:add-budget')
        return render(request, 'base_form.html', {
            'title': 'Add Budget',
            'form': form,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def edit_budget(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    data = {
        'amount': budget.amount,
    }
    if request.method == 'POST':
        form = BudgetForm(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    cleaned_data = form.cleaned_data[field]
                    if field == 'amount':
                        budget.amount = cleaned_data
                budget.save()
            return redirect('budget:budget')
    else:
        form = BudgetForm(data)
        form.helper.form_action = reverse('budget:edit-budget', kwargs={'budget_id': budget.id})
        return render(request, 'base_form.html', {
            'title': 'Edit Budget',
            'form': form,
            'budget_id': budget.id,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def delete_budget(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    budget.delete()
    return redirect('budget:budget')


@login_required(login_url='/budget/login/', redirect_field_name='next')
def add_item(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    if request.method == 'POST':
        form = ItemAddForm(request.POST)
        if form.is_valid():
            item_type = form.cleaned_data['type']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            creation_date = now()
            item = Item(budget=budget, amount=amount, type=item_type, description=description,
                        creation_date=creation_date)
            item.save()
            return redirect('budget:budget')
    else:
        form = ItemAddForm()
        form.helper.form_action = reverse('budget:add-item', kwargs={'budget_id': budget.id})
        return render(request, 'base_form.html', {
            'title': 'Add Item',
            'form': form,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def edit_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    data = {
        'type': item.type.id,
        'amount': item.amount,
        'description': item.description,
    }
    if request.method == 'POST':
        form = ItemEditForm(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    cleaned_data = form.cleaned_data[field]
                    if field == 'type':
                        item.item = cleaned_data
                    elif field == 'amount':
                        item.amount = cleaned_data
                    elif field == 'description':
                        item.description = cleaned_data
                item.save()
            return redirect('budget:budget')
    else:
        form = ItemEditForm(data)
        form.helper.form_action = reverse('budget:edit-item', kwargs={'item_id': item.id})
        return render(request, 'base_form.html', {
            'title': 'Edit Item',
            'form': form,
            'item_id': item.id,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def delete_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.delete()
    return redirect('budget:budget')


class TransactionsView(LoginRequiredMixin, TemplateView):
    login_url = '/budget/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = get_user_in_session(request.session)
        budget = get_budget_for_user(user)

        if budget is not None:
            user_id = request.session['_auth_user_id']
            user = User.objects.get(pk=user_id)
            budget = Budget.objects.get(user=user)

            today = now()
            current_month = today.month
            current_year = today.year
            transaction_list = budget.get_transactions_for_month_and_year(current_month, current_year)
            paginator = Paginator(transaction_list, 10)

            page = request.GET.get('page')
            try:
                transactions = paginator.page(page)
            except PageNotAnInteger:
                transactions = paginator.page(1)
            except EmptyPage:
                transactions = paginator.page(paginator.num_pages)

            return render_to_response('budget/transactions.html', {
                'title': 'Transactions',
                'user': user,
                'transaction_list': transaction_list,
                'transactions': transactions,
            })
        else:
            return render_to_response('budget/transactions.html', {
                'title': 'Transactions',
            })


@login_required(login_url='/budget/login/', redirect_field_name='next')
@json_view
def add_transaction(request):
    user = get_user_in_session(request.session)
    budget = get_budget_for_user(user)
    data = {'budget': budget}

    if request.method == 'POST':
        form = TransactionAddForm(request.POST, initial=data)
        if form.is_valid():
            item = form.cleaned_data['item']
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            new_york = timezone('America/New_York')
            transaction_date = form.cleaned_data['transaction_date'].astimezone(new_york)
            creation_date = now()
            transaction = Transaction(
                    item=item,
                    description=description,
                    amount=amount,
                    transaction_date=transaction_date,
                    creation_date=creation_date
            )
            transaction.save()
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
        form = TransactionAddForm(initial=data)
        return render(request, 'base_form.html', {
            'title': 'Add Transaction',
            'form': form,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def edit_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    user = get_user_in_session(request.session)
    budget = get_budget_for_user(user)
    data = {
        'item': transaction.item.id,
        'description': transaction.description,
        'amount': transaction.amount,
        'transaction_date': transaction.transaction_date,
        'budget': budget
    }
    if request.method == 'POST':
        form = TransactionEditForm(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    cleaned_data = form.cleaned_data[field]
                    if field == 'item':
                        transaction.item = cleaned_data
                    elif field == 'description':
                        transaction.description = cleaned_data
                    elif field == 'amount':
                        transaction.amount = cleaned_data
                    elif field == 'transaction_date':
                        transaction.transaction_date = cleaned_data
                transaction.save()
            return redirect('budget:transactions')
    else:
        form = TransactionEditForm(data, initial={'budget': budget})
        form.helper.form_action = reverse('budget:edit-transaction', kwargs={'transaction_id': transaction.id})
        return render(request, 'base_form.html', {
            'title': 'Edit Transaction',
            'form': form,
            'transaction_id': transaction.id,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.delete()
    return redirect('budget:transactions')


def get_user_in_session(session):
    user_id = session['_auth_user_id']
    user = User.objects.get(pk=user_id)
    return user


def get_budget_for_user(user):
    budget = None
    try:
        budget = Budget.objects.get(user=user)
    finally:
        if budget is None:
            return None
        else:
            return budget


def get_paginator_for_list(request, array_list, max_pages):
    paginator = Paginator(array_list, max_pages)

    page = request.GET.get('page')
    try:
        array = paginator.page(page)
    except PageNotAnInteger:
        array = paginator.page(1)
    except EmptyPage:
        array = paginator.page(paginator.num_pages)
    return array
