from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Item


def overview(request):
    user_id = None
    try:
        user_id = request.session['_auth_user_id']
    finally:
        if user_id is not None:
            user = User.objects.get(pk=user_id)
            items = Item.objects.filter(user=user)
            return render(request, 'budget/overview.html', {
                'user': user,
            })
        else:
            return render(request, 'budget/login.html')


def revenue(request):
    user_id = None
    try:
        user_id = request.session['_auth_user_id']
    finally:
        if user_id is not None:
            user = User.objects.get(pk=user_id)
            items = Item.objects.filter(user=user).filter(type=1)
            return render(request, 'budget/revenue.html', {
                'user': user,
                'items': items,
            })
        else:
            return render(request, 'budget/login.html')


def expenses(request):
    user_id = None
    try:
        user_id = request.session['_auth_user_id']
    finally:
        if user_id is not None:
            user = User.objects.get(pk=user_id)
            items = Item.objects.filter(user=user).filter(type=-1)
            return render(request, 'budget/expenses.html', {
                'user': user,
                'items': items,
            })
        else:
            return render(request, 'budget/login.html')


def add(request):
    user_id = None
    try:
        user_id = request.session['_auth_user_id']
    finally:
        if user_id is not None:
            user = User.objects.get(pk=user_id)
            return render(request, 'budget/add.html', {
                'user': user,
            })
        else:
            return render(request, 'budget/login.html')


def add_submit(request):
    print("User id: " + user)
    print(request)


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
