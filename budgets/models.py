from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=25)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name.title()


class Budget(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=35, blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'category'

    def __str__(self):
        return self.category.name.title()


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

    class Meta:
        ordering = ["transaction_date"]

    def __str__(self):
        return "budget=%s, description=%s, amount=%s, transaction_date=%s" \
               % (self.budget.category.name, self.description, self.amount, self.transaction_date)
