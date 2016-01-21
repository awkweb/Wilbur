from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum

from budgets.models import Budget, Category, Transaction


def get_user_in_session(session):
    user = None
    try:
        user_id = session['_auth_user_id']
        user = get_user_model().objects.get(pk=user_id)
    finally:
        return user


def get_budgets_for_user(user):
    budgets = None
    try:
        budgets = Budget.objects.filter(user=user).order_by('category__name')
    finally:
        return budgets


def get_transactions_with_month_and_year(user, month, year):
    transactions = Transaction.objects.filter(budget__user=user).filter(transaction_date__year=year)\
        .filter(transaction_date__month=month).order_by('-transaction_date')
    return transactions


def get_transactions_for_budget_with_month_and_year(budget, month, year):
    transactions = Transaction.objects.filter(budget=budget).filter(transaction_date__year=year)\
        .filter(transaction_date__month=month)
    return transactions


def get_sum_transactions_for_budget_with_month_and_year(budget, month, year):
    transactions = Transaction.objects.filter(budget=budget).filter(transaction_date__year=year)\
        .filter(transaction_date__month=month)
    total = transactions.aggregate(Sum('amount'))['amount__sum']
    total = int(total) if total is not None else 0
    return total


def get_unused_categories_for_user(user, current_budget=None):
    budgets = get_budgets_for_user(user)
    budget_categories = []
    for budget in budgets:
        budget_categories.append(budget.category.id)
    if current_budget:
        budget_categories.remove(current_budget.id)
    categories = Category.objects.exclude(pk__in=budget_categories).order_by('name')
    return categories


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
