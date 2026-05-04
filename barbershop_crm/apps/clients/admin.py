from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'loyalty_tier', 'total_spent', 'visit_count', 'created_at']
    list_filter = ['loyalty_tier']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    readonly_fields = ['total_spent', 'visit_count', 'created_at', 'updated_at']
