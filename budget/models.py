from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):
    user = models.ForeignKey(User)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    creation_date = models.DateTimeField()

    def __str__(self):
        return "user=%s" % self.user

    def get_items(self):
        items = Item.objects.filter(budget=self)
        return items

    def get_total_for_transactions(self):
        items = self.get_budget_items()
        total = 0
        for item in items:
            total += item.amount
        return total


class ItemType(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    def __str__(self):
        return "name=%s" % self.name


class Item(models.Model):
    budget = models.ForeignKey(Budget)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    type = models.ForeignKey(ItemType)
    description = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField()

    def __str__(self):
        return "budget=%s, amount=%s, type=%s" % (self.budget, self.amount, self.type)

    def get_transactions(self):
        transactions = Transaction.objects.filter(item=self)
        return transactions


class Transaction(models.Model):
    item = models.ForeignKey(Item)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    transaction_date = models.DateTimeField()
    creation_date = models.DateTimeField()

    EXPENSE = -1
    REVENUE = 1
    TYPE_CHOICES = (
        (EXPENSE, 'Expense'),
        (REVENUE, 'Revenue'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES,
                               default=EXPENSE)

    def __str__(self):
        return "name=%s, amount=%s, type=%s" % (self.name, self.amount, self.type)
