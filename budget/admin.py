from django.contrib import admin

from .models import Budget, ItemType, Item, Transaction


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount',)


class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': ['budget', 'type', 'amount', 'description', 'creation_date']}),
    ]
    list_display = ('budget', 'type', 'amount', 'description', 'creation_date',)
    list_filter = ['type', 'amount', 'creation_date']


class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
            {'fields': ['budget_item', 'type', 'name', 'amount', 'transaction_date', 'creation_date']}),
    ]
    list_display = ('item', 'name', 'amount', 'transaction_date', 'type',)
    list_filter = ['type', 'amount', 'transaction_date']

admin.site.register(Budget, BudgetAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Transaction, TransactionAdmin)
