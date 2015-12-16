"""wilbur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='overview'),

    url(r'^budget/$', views.BudgetView.as_view(), name='budget'),
    url(r'^budget/add/$', views.add_budget, name='add-budget'),
    url(r'^budget/edit/(?P<budget_id>[0-9]+)/$', views.edit_budget, name='edit-budget'),
    url(r'^budget/delete/(?P<budget_id>[0-9]+)/$', views.delete_budget, name='delete-budget'),

    url(r'^budget/(?P<budget_id>[0-9]+)/item/add/$', views.add_item, name='add-item'),
    url(r'^budget/item/edit/(?P<item_id>[0-9]+)/$', views.edit_item, name='edit-item'),
    url(r'^budget/item/delete/(?P<item_id>[0-9]+)/$', views.delete_item, name='delete-item'),

    url(r'^transactions/$', views.TransactionsView.as_view(), name='transactions'),
    url(r'^transactions/add/$', views.add_transaction, name='add-transaction'),
    url(r'^transactions/edit/(?P<transaction_id>[0-9]+)/$', views.edit_transaction, name='edit-transaction'),
    url(r'^transactions/delete/(?P<transaction_id>[0-9]+)/$', views.delete_transaction, name='delete-transaction'),

    url('^login/$', auth_views.login, {
        'template_name': 'budget/login.html',
        'redirect_field_name': 'next'}, name="login"),
    url('^logout/$', auth_views.logout, {'next_page': '/budget/'}, name="logout", ),
]
