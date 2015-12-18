from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=75)
    creation_date = models.DateField()

    def __str__(self):
        return self.name


class Budget(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True)
    creation_date = models.DateField()

    def __str__(self):
        return self.category.name

    def get_transactions_for_month_and_year(self, month, year):
        items = self.get_items()
        transaction_list = []
        for item in items:
            transactions = item.get_transactions_for_month_and_year(month, year)
            for transaction in transactions:
                transaction_list.append(transaction)
        return sorted(transaction_list, reverse=True, key=lambda t: t.transaction_date)

    def get_sum_transactions_for_month_and_year(self, month, year):
        items = self.get_items()
        total = 0
        for item in items:
            total += item.get_sum_transactions_for_month_and_year(month, year)
        return total

    def get_percent_spent(self):
        total = self.get_sum_transactions()
        return total / self.amount * 100


class Transaction(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True)
    transaction_date = models.DateField()
    creation_date = models.DateField()

    EXPENSE = -1
    REVENUE = 1
    TYPE_CHOICES = (
        (EXPENSE, 'Expense'),
        (REVENUE, 'Revenue'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES,
                               default=EXPENSE)

    def __str__(self):
        return "description=%s, amount=%s, type=%s" % (self.description, self.amount, self.type)
