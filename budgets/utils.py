from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Budget, Category


def get_user_in_session(session):
    user = None
    try:
        user_id = session['_auth_user_id']
        user = User.objects.get(pk=user_id)
    finally:
        return user


def get_budgets_for_user(user):
    budgets = None
    try:
        budgets = Budget.objects.filter(user=user).order_by('category__name')
    finally:
        return budgets


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
