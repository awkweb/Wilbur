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

    def get_transactions(self):
        items = self.get_items()
        transaction_list = []
        for item in items:
            transactions = item.get_transactions()
            for transaction in transactions:
                transaction_list.append(transaction)
        return sorted(transaction_list, reverse=True, key=lambda t: t.transaction_date)

    def get_sum_transactions(self):
        items = self.get_items()
        total = 0
        for item in items:
            total += item.get_sum_transactions()
        return total

    def get_percent_spent(self):
        total = self.get_sum_transactions()
        return total / self.amount * 100


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

    def get_sum_transactions(self):
        transactions = self.get_transactions()
        total = 0
        for transaction in transactions:
            total += transaction.amount
        return total

    def get_percent_spent(self):
        total = self.get_sum_transactions()
        return total / self.amount * 100


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
