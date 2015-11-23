from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    date = models.DateTimeField('date created')

    EXPENSE = -1
    REVENUE = 1
    TYPE_CHOICES = (
        (EXPENSE, 'Expense'),
        (REVENUE, 'Revenue'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES,
                               default=REVENUE)

    MONTHLY = 12
    BIMONTHLY = 6
    ONETIME = 1
    FREQUENCY_CHOICES = (
        (MONTHLY, 'Monthly'),
        (BIMONTHLY, 'Bi-monthly'),
        (ONETIME, 'One-time'),
    )
    frequency = models.IntegerField(choices=FREQUENCY_CHOICES,
                                    default=MONTHLY)

    def __str__(self):
        return "Name: %s, type: %s, amount: %s, frequency: %s" % (self.name, self.type, self.amount, self.frequency)
