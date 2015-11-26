# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_budget_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='budget_item',
            new_name='item',
        ),
        migrations.AlterField(
            model_name='budget',
            name='amount',
            field=models.DecimalField(max_digits=10, verbose_name='Amount', decimal_places=2),
        ),
    ]
