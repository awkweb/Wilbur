from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

from budget.models import Budget


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = None
        try:
            user_id = request.session['_auth_user_id']
        finally:
            if user_id is not None:
                user = User.objects.get(pk=user_id)
                budget = Budget.objects.get(user=user)
                transactions = budget.get_transactions()[:4]
                return render(request, 'budget/overview.html', {
                    'budget': budget,
                    'transactions': transactions,
                })
            else:
                return render(request, 'budget/login.html')


class BudgetView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = request.session['_auth_user_id']
        user = User.objects.get(pk=user_id)
        budget = Budget.objects.get(user=user)
        items = budget.get_items()
        return render(request, 'budget/budget.html', {
            'budget': budget,
            'items': items,
        })


class TransactionsView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = request.session['_auth_user_id']
        user = User.objects.get(pk=user_id)
        budget = Budget.objects.get(user=user)
        transactions = budget.get_transactions()
        return render(request, 'budget/transactions.html', {
            'transactions': transactions,
        })


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
