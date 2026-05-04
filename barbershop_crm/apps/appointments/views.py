import json
from datetime import datetime, timedelta
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .models import Appointment, AppointmentStatus
from .forms import AppointmentForm
from apps.staff.models import Master
from apps.accounts.mixins import (
    ManagerRequiredMixin, get_user_role, get_master_profile, is_master,
)


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/list.html'
    context_object_name = 'appointments'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related('client', 'master', 'service')

        if is_master(self.request.user):
            master = get_master_profile(self.request.user)
            qs = qs.filter(master=master) if master else qs.none()

        status    = self.request.GET.get('status', '')
        master_id = self.request.GET.get('master', '')
        date      = self.request.GET.get('date', '')
        if status:
            qs = qs.filter(status=status)
        if master_id and not is_master(self.request.user):
            qs = qs.filter(master_id=master_id)
        if date:
            qs = qs.filter(start_time__date=date)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['masters']       = Master.objects.filter(is_active=True)
        ctx['statuses']      = AppointmentStatus.choices
        ctx['status_filter'] = self.request.GET.get('status', '')
        ctx['master_filter'] = self.request.GET.get('master', '')
        ctx['date_filter']   = self.request.GET.get('date', '')
        return ctx


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'appointments/calendar.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        masters = Master.objects.filter(is_active=True).order_by('calendar_order')
        # Master sees only their own column
        if is_master(self.request.user):
            own = get_master_profile(self.request.user)
            if own:
                masters = masters.filter(pk=own.pk)
        ctx['masters'] = masters
        return ctx


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/detail.html'
    context_object_name = 'appointment'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if is_master(self.request.user):
            master = get_master_profile(self.request.user)
            if not master or obj.master_id != master.pk:
                raise PermissionDenied
        return obj


class AppointmentCreateView(ManagerRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Запись создана')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('appointments:detail', kwargs={'pk': self.object.pk})


class AppointmentUpdateView(ManagerRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Запись обновлена')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('appointments:detail', kwargs={'pk': self.object.pk})


# ---- JSON API ----

class AppointmentEventsAPIView(LoginRequiredMixin, View):
    def get(self, request):
        start_str = request.GET.get('start', '')
        end_str   = request.GET.get('end', '')
        master_id = request.GET.get('master', '')
        try:
            from django.utils.timezone import make_aware
            start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end   = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            if start.tzinfo is None:
                start = make_aware(start)
            if end.tzinfo is None:
                end = make_aware(end)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid date'}, status=400)

        qs = Appointment.objects.filter(
            start_time__gte=start, start_time__lt=end
        ).select_related('client', 'master', 'service').exclude(
            status=AppointmentStatus.CANCELLED
        )

        # Master: force filter to own appointments
        if is_master(request.user):
            own = get_master_profile(request.user)
            qs = qs.filter(master=own) if own else qs.none()
        elif master_id:
            qs = qs.filter(master_id=master_id)

        return JsonResponse([a.to_fullcalendar_event() for a in qs], safe=False)


class AppointmentStatusAPIView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)

        # Master can only change own appointments
        if is_master(request.user):
            own = get_master_profile(request.user)
            if not own or appt.master_id != own.pk:
                return JsonResponse({'error': 'Forbidden'}, status=403)

        try:
            data       = json.loads(request.body)
            new_status = data.get('status', '')
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'error': 'Bad request'}, status=400)

        if new_status not in AppointmentStatus.values:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        appt.status = new_status
        appt.save(update_fields=['status', 'updated_at'])
        return JsonResponse({
            'success': True,
            'status':  appt.status,
            'label':   appt.get_status_display(),
            'color':   appt.status_color,
        })


class AppointmentMoveAPIView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)

        # Master can only move own appointments
        if is_master(request.user):
            own = get_master_profile(request.user)
            if not own or appt.master_id != own.pk:
                return JsonResponse({'error': 'Forbidden'}, status=403)

        try:
            data      = json.loads(request.body)
            from django.utils import timezone as tz
            new_start = datetime.fromisoformat(data['start'].replace('Z', '+00:00'))
            new_end   = datetime.fromisoformat(data['end'].replace('Z', '+00:00'))
            if new_start.tzinfo is None:
                new_start = tz.make_aware(new_start)
            if new_end.tzinfo is None:
                new_end = tz.make_aware(new_end)
            new_master_id = data.get('resourceId', appt.master_id)
        except (json.JSONDecodeError, KeyError, ValueError):
            return JsonResponse({'error': 'Bad request'}, status=400)

        # Master cannot reassign to another master
        if is_master(request.user):
            own = get_master_profile(request.user)
            new_master_id = own.pk if own else appt.master_id

        appt.start_time = new_start
        appt.end_time   = new_end
        appt.master_id  = new_master_id
        appt.save(update_fields=['start_time', 'end_time', 'master_id', 'updated_at'])
        return JsonResponse({'success': True})
