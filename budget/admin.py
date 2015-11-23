from django.contrib import admin

from .models import Item


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Item information',
            {'fields': ['user', 'type', 'frequency', 'name', 'amount', 'date']}),
    ]
    list_display = ('user', 'name', 'type', 'frequency', 'amount')
    list_filter = ['type', 'frequency', 'amount', 'date']

admin.site.register(Item, ItemAdmin)
