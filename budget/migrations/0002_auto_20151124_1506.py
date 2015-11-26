# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='creation_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='creation_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='creation_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='creation_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(),
        ),
    ]
