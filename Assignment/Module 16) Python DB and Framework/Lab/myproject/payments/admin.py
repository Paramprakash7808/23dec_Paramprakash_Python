from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_id',)
    readonly_fields = ('order_id', 'amount', 'status', 'checksum', 'created_at')
