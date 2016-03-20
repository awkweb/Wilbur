from django.conf.urls import url
from django.contrib.auth import views as auth_views

from budgets import views
from cuser.forms import UserAuthenticationForm

urlpatterns = [
    url(r'^$', views.OverviewView.as_view(), name='overview'),

    url(r'^budgets/$', views.BudgetsView.as_view(), name='budgets'),
    url(r'^budgets/add/$', views.BudgetsAddView.as_view(), name='budgets-add'),
    url(r'^budgets/edit/(?P<budget_id>[0-9]+)/$', views.BudgetsEditView.as_view(), name='budgets-edit'),
    url(r'^budgets/delete/(?P<budget_id>[0-9]+)/$', views.delete_budget, name='budgets-delete'),

    url(r'^transactions/$', views.TransactionsView.as_view(), name='transactions'),
    url(r'^transactions/add/$', views.TransactionsAddView.as_view(), name='transactions-add'),
    url(r'^transactions/edit/(?P<transaction_id>[0-9]+)/$', views.TransactionsEditView.as_view(), name='transactions-edit'),
    url(r'^transactions/delete/(?P<transaction_id>[0-9]+)/$', views.delete_transaction, name='transactions-delete'),
    url(r'^transactions/budget/(?P<budget_id>[0-9]+)/$', views.TransactionsView.as_view(), name='transactions-budget'),

    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/password/$', views.PasswordEditView.as_view(), name='profile-password-edit'),

    url('^signup/$', views.SignUpView.as_view(), name="signup"),
    url('^login/$', auth_views.login, {
        'template_name': 'registration/login.html',
        'redirect_field_name': 'next',
        'authentication_form': UserAuthenticationForm,
    }, name="login"),
    url('^logout/$', auth_views.logout, {'next_page': '/'}, name="logout"),

    url(r'^style-guide/$', views.StyleGuideView.as_view(), name='style'),
]
