# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('creation_date', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('amount', models.DecimalField(max_digits=10, verbose_name='Amount', decimal_places=2)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('creation_date', models.DateField()),
                ('budget', models.ForeignKey(to='budget.Budget')),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('creation_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(max_digits=10, verbose_name='Amount', decimal_places=2)),
                ('transaction_date', models.DateField()),
                ('creation_date', models.DateField()),
                ('type', models.IntegerField(default=-1, choices=[(-1, 'Expense'), (1, 'Revenue')])),
                ('budget_item', models.ForeignKey(to='budget.Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(to='budget.ItemType'),
        ),
    ]
