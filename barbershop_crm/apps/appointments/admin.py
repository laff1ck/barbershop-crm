from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['client', 'master', 'service', 'start_time', 'status']
    list_filter = ['status', 'master', 'start_time']
    search_fields = ['client__first_name', 'client__last_name', 'client__phone']
    date_hierarchy = 'start_time'
