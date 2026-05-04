import csv
from datetime import timedelta, datetime
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.contrib import messages
from .models import Payment, PaymentMethod
from .forms import PaymentForm
from apps.appointments.models import Appointment
from apps.staff.models import Master
from apps.accounts.mixins import ManagerRequiredMixin


class PaymentListView(ManagerRequiredMixin, ListView):
    model = Payment
    template_name = 'billing/list.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_queryset(self):
        qs = Payment.objects.select_related(
            'appointment__client', 'appointment__master', 'appointment__service'
        ).order_by('-paid_at')
        master_id = self.request.GET.get('master', '')
        date_from  = self.request.GET.get('date_from', '')
        date_to    = self.request.GET.get('date_to', '')
        if master_id:
            qs = qs.filter(appointment__master_id=master_id)
        if date_from:
            qs = qs.filter(paid_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(paid_at__date__lte=date_to)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['masters']       = Master.objects.filter(is_active=True)
        ctx['master_filter'] = self.request.GET.get('master', '')
        ctx['date_from']     = self.request.GET.get('date_from', '')
        ctx['date_to']       = self.request.GET.get('date_to', '')
        return ctx


class PaymentDetailView(ManagerRequiredMixin, DetailView):
    model = Payment
    template_name = 'billing/detail.html'
    context_object_name = 'payment'


class PaymentCreateView(ManagerRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'billing/form.html'

    def get_appointment(self):
        return get_object_or_404(Appointment, pk=self.kwargs['appt_pk'])

    def get_initial(self):
        appt = self.get_appointment()
        return {'amount': appt.service.price}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['appointment'] = self.get_appointment()
        return ctx

    def form_valid(self, form):
        from django.db import transaction
        from django.utils import timezone

        appt = self.get_appointment()
        form.instance.appointment = appt

        with transaction.atomic():
            response = super().form_valid(form)

            # Обновляем клиента
            client = appt.client
            client.visit_count += 1
            client.total_spent = (client.total_spent or 0) + self.object.final_amount
            client.last_visit  = timezone.localdate()
            client.save(update_fields=['visit_count', 'total_spent', 'last_visit'])
            client.recalculate_tier()

        messages.success(self.request, 'Платёж записан')
        return response

    def get_success_url(self):
        return reverse_lazy('billing:detail', kwargs={'pk': self.object.pk})


class ReportsView(ManagerRequiredMixin, TemplateView):
    template_name = 'billing/reports.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today       = timezone.localdate()
        month_start = today.replace(day=1)

        # ── Date range + master filter ─────────────────────────────────────────
        date_from_str = self.request.GET.get('date_from', '')
        date_to_str   = self.request.GET.get('date_to', '')
        master_id     = self.request.GET.get('master', '')

        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date() if date_from_str else month_start
        except ValueError:
            date_from = month_start
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date() if date_to_str else today
        except ValueError:
            date_to = today

        ctx['date_from']     = date_from.strftime('%Y-%m-%d')
        ctx['date_to']       = date_to.strftime('%Y-%m-%d')
        ctx['master_filter'] = master_id
        ctx['masters']       = Master.objects.filter(is_active=True)

        base_qs = Payment.objects.filter(paid_at__date__gte=date_from, paid_at__date__lte=date_to)
        if master_id:
            base_qs = base_qs.filter(appointment__master_id=master_id)

        # ── Daily revenue chart ────────────────────────────────────────────────
        daily = (
            base_qs
            .annotate(day=TruncDate('paid_at'))
            .values('day')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('day')
        )
        ctx['daily_labels'] = [str(r['day']) for r in daily]
        ctx['daily_totals'] = [float(r['total']) for r in daily]

        # ── Master breakdown ───────────────────────────────────────────────────
        master_rows = (
            base_qs
            .values('appointment__master__pk', 'appointment__master__display_name', 'appointment__master__color')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')
        )
        master_stats = []
        for row in master_rows:
            cnt = row['count'] or 1
            master_stats.append({
                'pk':    row['appointment__master__pk'],
                'name':  row['appointment__master__display_name'],
                'color': row['appointment__master__color'],
                'total': row['total'],
                'count': row['count'],
                'avg':   round(float(row['total']) / cnt, 2),
            })
        ctx['master_stats']   = master_stats
        ctx['master_labels']  = [r['name'] for r in master_stats]
        ctx['master_totals_chart'] = [float(r['total']) for r in master_stats]
        ctx['master_colors']  = [r['color'] for r in master_stats]

        # ── Top masters (legacy, keep for top-5 list) ─────────────────────────
        ctx['top_masters'] = master_stats[:5]

        # ── Top clients ───────────────────────────────────────────────────────
        ctx['top_clients'] = (
            base_qs
            .values('appointment__client__first_name', 'appointment__client__last_name', 'appointment__client__pk')
            .annotate(total=Sum('amount'), visits=Count('id'))
            .order_by('-total')[:10]
        )

        ctx['month_revenue'] = base_qs.aggregate(total=Sum('amount'))['total'] or 0
        ctx['month_count']   = base_qs.count()

        # Средний чек за день = выручка / кол-во дней в периоде
        period_days = max((date_to - date_from).days + 1, 1)
        ctx['avg_daily'] = round(float(ctx['month_revenue']) / period_days, 2) if ctx['month_revenue'] else 0

        # Средний чек за визит = выручка / кол-во оплат
        ctx['avg_check'] = round(float(ctx['month_revenue']) / ctx['month_count'], 2) if ctx['month_count'] else 0

        return ctx


class ExportCSVView(ManagerRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="payments.csv"'
        writer = csv.writer(response)
        writer.writerow(['Чек', 'Дата', 'Клиент', 'Мастер', 'Услуга', 'Сумма', 'Скидка%', 'Итого', 'Способ'])
        for p in Payment.objects.select_related(
            'appointment__client', 'appointment__master', 'appointment__service'
        ).order_by('-paid_at'):
            writer.writerow([
                p.receipt_number,
                p.paid_at.strftime('%d.%m.%Y %H:%M'),
                p.appointment.client.full_name,
                p.appointment.master.display_name,
                p.appointment.service.name,
                str(p.amount),
                str(p.discount),
                str(p.final_amount),
                p.get_method_display(),
            ])
        return response
