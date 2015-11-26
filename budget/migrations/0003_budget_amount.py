# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_auto_20151124_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='amount',
            field=models.DecimalField(max_digits=10, verbose_name='Amount', decimal_places=2, default=0),
        ),
    ]
