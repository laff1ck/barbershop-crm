from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum, Count, Q


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.appointments.models import Appointment, AppointmentStatus
        from apps.billing.models import Payment
        from apps.clients.models import Client
        from apps.staff.models import Master

        today = timezone.localdate()
        month_start = today.replace(day=1)

        today_appts = Appointment.objects.filter(
            start_time__date=today
        ).select_related('client', 'master', 'service').order_by('start_time')

        today_revenue = Payment.objects.filter(
            paid_at__date=today
        ).aggregate(total=Sum('amount'))['total'] or 0

        month_revenue = Payment.objects.filter(
            paid_at__date__gte=month_start
        ).aggregate(total=Sum('amount'))['total'] or 0

        ctx.update({
            'today': today,
            'today_appointments': today_appts,
            'today_revenue': today_revenue,
            'month_revenue': month_revenue,
            'appointments_today_count': today_appts.count(),
            'in_progress_count': today_appts.filter(status=AppointmentStatus.IN_PROGRESS).count(),
            'new_clients_month': Client.objects.filter(
                created_at__date__gte=month_start
            ).count(),
            'total_clients': Client.objects.count(),
            'active_masters': Master.objects.filter(is_active=True).count(),
            'recent_appointments': today_appts[:10],
        })
        return ctx
