# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='frequency',
            field=models.IntegerField(default=12, choices=[(12, 'Monthly'), (6, 'Bi-monthly'), (1, 'One-time')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.IntegerField(default=1, choices=[(-1, 'Expense'), (1, 'Revenue')]),
        ),
    ]
