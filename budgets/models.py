from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=25)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name.title()


class Budget(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=35, blank=True)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category.name.title()

    def get_transactions_for_month_and_year(self, month, year):
        transactions = Transaction.objects.filter(budget=self).filter(transaction_date__year=year)\
            .filter(transaction_date__month=month)
        return transactions

    def get_sum_transactions_for_month_and_year(self, month, year):
        transactions = Transaction.objects.filter(budget=self).filter(transaction_date__year=year)\
            .filter(transaction_date__month=month)
        total = 0
        for transaction in transactions:
            total += transaction.amount
        return total


class Transaction(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50, blank=True)
    transaction_date = models.DateField()
    creation_date = models.DateField(auto_now_add=True)

    EXPENSE = -1
    REVENUE = 1
    TYPE_CHOICES = (
        (EXPENSE, 'Expense'),
        (REVENUE, 'Revenue'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES,
                               default=EXPENSE)

    def __str__(self):
        return "budget=%s, description=%s, amount=%s, transaction_date=%s" \
               % (self.budget.category.name, self.description, self.amount, self.transaction_date)