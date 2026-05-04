from django.contrib import admin
from .models import Master, Specialization, WorkSchedule, DayOff


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'phone', 'rating', 'is_active', 'calendar_order']
    list_editable = ['is_active', 'calendar_order']
    filter_horizontal = ['specializations']


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ['master', 'weekday', 'start_time', 'end_time', 'is_day_off']


@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    list_display = ['master', 'date', 'reason']
