from django.contrib import admin

from .models import Budget, Category, Transaction


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': ['budget', 'description', 'amount', 'transaction_date']}),
    ]
    list_display = ('budget', 'description', 'amount', 'transaction_date',)
    list_filter = ['amount', 'transaction_date']

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)

