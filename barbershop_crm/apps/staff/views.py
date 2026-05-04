from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Master
from .forms import MasterForm
from apps.accounts.mixins import AdminRequiredMixin, get_master_profile, is_master


class MasterListView(LoginRequiredMixin, ListView):
    model = Master
    template_name = 'staff/list.html'
    context_object_name = 'masters'
    queryset = Master.objects.filter(is_active=True).prefetch_related('specializations', 'services')


class MasterDetailView(LoginRequiredMixin, DetailView):
    model = Master
    template_name = 'staff/detail.html'
    context_object_name = 'master'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Master can only view their own profile
        if is_master(self.request.user):
            own = get_master_profile(self.request.user)
            if not own or own.pk != obj.pk:
                raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.appointments.models import Appointment
        from django.utils import timezone
        from django.db.models import Sum
        from apps.billing.models import Payment
        today = timezone.localdate()
        ctx['today_appointments'] = (
            self.object.appointments
            .filter(start_time__date=today)
            .select_related('client', 'service')
            .order_by('start_time')
        )
        ctx['total_revenue'] = Payment.objects.filter(
            appointment__master=self.object
        ).aggregate(total=Sum('amount'))['total'] or 0
        ctx['total_appointments'] = self.object.appointments.count()
        return ctx


class MasterCreateView(AdminRequiredMixin, CreateView):
    model = Master
    form_class = MasterForm
    template_name = 'staff/form.html'
    success_url = reverse_lazy('staff:list')

    def form_valid(self, form):
        messages.success(self.request, 'Мастер добавлен')
        return super().form_valid(form)


class MasterUpdateView(AdminRequiredMixin, UpdateView):
    model = Master
    form_class = MasterForm
    template_name = 'staff/form.html'

    def get_success_url(self):
        messages.success(self.request, 'Данные мастера обновлены')
        return reverse_lazy('staff:detail', kwargs={'pk': self.object.pk})
