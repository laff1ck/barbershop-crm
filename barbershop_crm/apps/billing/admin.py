from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'appointment', 'amount', 'method', 'paid_at']
    list_filter = ['method', 'paid_at']
    readonly_fields = ['receipt_number', 'paid_at']
