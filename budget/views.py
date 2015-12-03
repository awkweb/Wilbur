from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from pytz import timezone
import pytz
from .models import Budget, Transaction, Item
from .forms import TransactionForm, BudgetForm, ItemForm


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/budget/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user_id = request.session['_auth_user_id']
        user = User.objects.get(pk=user_id)
        budget = Budget.objects.get(user=user)

        today = now()
        current_month = today.month
        current_year = today.year
        transactions = budget.get_transactions_for_month_and_year(current_month, current_year)[:4]
        total_spent = budget.get_sum_transactions_for_month_and_year(current_month, current_year)
        spent_percentage = total_spent / budget.amount * 100
        return render(request, 'budget/overview.html', {
            'budget': budget,
            'transactions': transactions,
            'total_spent': total_spent,
            'spent_percentage': spent_percentage,
        })


class BudgetView(LoginRequiredMixin, TemplateView):
    login_url = '/budget/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user_id = request.session['_auth_user_id']
        user = User.objects.get(pk=user_id)
        budget = Budget.objects.get(user=user)

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
            'budget': budget,
            'total_spent': total_spent,
            'spent_percentage': spent_percentage,
            'item_list': item_list,
        })


class TransactionsView(LoginRequiredMixin, TemplateView):
    login_url = '/budget/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
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
            'transaction_list': transaction_list,
            'transactions': transactions,
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
        return render(request, 'forms/edit-budget.html', {
            'form': form,
            'budget_id': budget.id,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def add_item(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    if request.method == 'POST':
        form = ItemForm(request.POST)
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
        form = ItemForm()
        return render(request, 'forms/add-item.html', {
            'form': form,
            'budget_id': budget.id,
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
        form = ItemForm(request.POST, initial=data)
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
        form = ItemForm(data)
        return render(request, 'forms/edit-item.html', {
            'form': form,
            'item_id': item.id,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def delete_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.delete()
    return redirect('budget:budget')


@login_required(login_url='/budget/login/', redirect_field_name='next')
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            new_york = timezone('America/New_York')
            transaction_date = form.cleaned_data['transaction_date'].astimezone(new_york)
            creation_date = now()
            transaction = Transaction(item=item, description=description, amount=amount,
                                      transaction_date=transaction_date,
                                      creation_date=creation_date)
            transaction.save()
            return redirect('budget:transactions')
    else:
        form = TransactionForm()
        return render(request, 'forms/add-transaction.html', {
            'form': form,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def edit_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    data = {
        'item': transaction.item.id,
        'description': transaction.description,
        'amount': transaction.amount,
        'transaction_date': transaction.transaction_date,
    }
    if request.method == 'POST':
        form = TransactionForm(request.POST, initial=data)
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
        form = TransactionForm(data)
        return render(request, 'forms/edit-transaction.html', {
            'form': form,
            'transaction_id': transaction.id,
        })


@login_required(login_url='/budget/login/', redirect_field_name='next')
def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.delete()
    return redirect('budget:transactions')
