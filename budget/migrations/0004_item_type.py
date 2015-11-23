# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_remove_item_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.IntegerField(choices=[(-1, 'Expense'), (1, 'Revenue')], default=1),
        ),
    ]
