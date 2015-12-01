from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from pytz import timezone
import pytz

from .models import Budget, Transaction
from .forms import AddTransactionForm


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = None
        try:
            user_id = request.session['_auth_user_id']
        finally:
            if user_id is not None:
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
            else:
                return render(request, 'budget/login.html')


class BudgetView(TemplateView):
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
            item_list.append((item.type.name, item.amount, item_total_spent, item_spent_percentage))
        return render(request, 'budget/budget.html', {
            'budget': budget,
            'total_spent': total_spent,
            'spent_percentage': spent_percentage,
            'item_list': item_list,
        })


class TransactionsView(TemplateView):
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


def edit_budget(request):
    return render(request, 'forms/edit-budget.html')


def add_transaction(request):
    if request.method == 'POST':
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            name = form.cleaned_data['name']
            amount = form.cleaned_data['amount']
            new_york = timezone('America/New_York')
            transaction_date = form.cleaned_data['transaction_date'].astimezone(new_york)
            creation_date = now()
            transaction = Transaction(item=item, name=name, amount=amount, transaction_date=transaction_date,
                                      creation_date=creation_date)
            transaction.save()
            return redirect('budget:transactions')
    else:
        form = AddTransactionForm()
        return render(request, 'forms/add-transaction.html', {
            'form': form,
        })


def edit_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    data = {
        'item': transaction.item.id,
        'name': transaction.name,
        'amount': transaction.amount,
        'transaction_date': transaction.transaction_date,
    }
    if request.method == 'POST':
        form = AddTransactionForm(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    cleaned_data = form.cleaned_data[field]
                    if field == 'item':
                        transaction.item = cleaned_data
                    elif field == 'name':
                        transaction.name = cleaned_data
                    elif field == 'amount':
                        transaction.amount = cleaned_data
                    elif field == 'transaction_date':
                        transaction.transaction_date = cleaned_data
                transaction.save()
            return redirect('budget:transactions')
    else:
        form = AddTransactionForm(data)
        return render(request, 'forms/edit-transaction.html', {
            'form': form,
            'transaction_id': transaction.id,
        })


def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.delete()
    return redirect('budget:transactions')


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/budget/')
        else:
            return render(request, 'budget/login.html', {
                'error_message': "Disabled account",
            })
    else:
        return render(request, 'budget/login.html', {
            'error_message': "Invalid credentials",
        })


def logout_user(request):
    logout(request)
    return redirect('/budget/')
