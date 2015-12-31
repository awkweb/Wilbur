from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^budgets/$', views.BudgetsView.as_view(), name='budgets'),
    url(r'^budgets/add/$', views.add_budget, name='add-budget'),
    url(r'^budgets/edit/(?P<budget_id>[0-9]+)/$', views.edit_budget, name='edit-budget'),
    url(r'^budgets/delete/(?P<budget_id>[0-9]+)/$', views.delete_budget, name='delete-budget'),

    url(r'^transactions/$', views.TransactionsView.as_view(), name='transactions'),
    url(r'^transactions/add/$', views.add_transaction, name='add-transaction'),
    url(r'^transactions/edit/(?P<transaction_id>[0-9]+)/$', views.edit_transaction, name='edit-transaction'),
    url(r'^transactions/delete/(?P<transaction_id>[0-9]+)/$', views.delete_transaction, name='delete-transaction'),

    url('^login/$', auth_views.login, {
        'template_name': 'budget/login.html',
        'redirect_field_name': 'next'}, name="login"),
    url('^logout/$', auth_views.logout, {'next_page': '/transactions/'}, name="logout"),
]
