from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Client
from .forms import ClientForm
from apps.accounts.mixins import (
    ManagerRequiredMixin, AdminRequiredMixin,
    get_user_role, get_master_profile, is_master,
)
from apps.accounts.models import Role


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('preferred_master')

        # Master sees only clients who had appointments with them
        if is_master(self.request.user):
            master = get_master_profile(self.request.user)
            if master:
                qs = qs.filter(appointments__master=master).distinct()
            else:
                qs = qs.none()

        from django.utils import timezone
        from datetime import timedelta

        q         = self.request.GET.get('q', '').strip()
        tier      = self.request.GET.get('tier', '')
        last_visit = self.request.GET.get('last_visit', '')

        if q:
            qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(phone__icontains=q))
        if tier:
            qs = qs.filter(loyalty_tier=tier)

        today = timezone.now().date()
        if last_visit == '7':
            qs = qs.filter(last_visit__gte=today - timedelta(days=7))
        elif last_visit == '30':
            qs = qs.filter(last_visit__gte=today - timedelta(days=30))
        elif last_visit == '90':
            qs = qs.filter(last_visit__gte=today - timedelta(days=90))
        elif last_visit == 'old':
            qs = qs.filter(last_visit__lt=today - timedelta(days=90))
        elif last_visit == 'never':
            qs = qs.filter(last_visit__isnull=True)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .models import LoyaltyTier
        ctx['q']               = self.request.GET.get('q', '')
        ctx['tier_filter']     = self.request.GET.get('tier', '')
        ctx['last_visit_filter'] = self.request.GET.get('last_visit', '')
        ctx['loyalty_tiers']   = LoyaltyTier.choices
        return ctx


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'client'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if is_master(self.request.user):
            master = get_master_profile(self.request.user)
            if not master or not obj.appointments.filter(master=master).exists():
                raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['appointments'] = (
            self.object.appointments
            .select_related('master', 'service')
            .order_by('-start_time')[:20]
        )
        return ctx


class ClientCreateView(ManagerRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/form.html'

    def get_success_url(self):
        messages.success(self.request, 'Клиент успешно добавлен')
        return reverse_lazy('clients:detail', kwargs={'pk': self.object.pk})


class ClientUpdateView(ManagerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/form.html'

    def get_success_url(self):
        messages.success(self.request, 'Данные клиента обновлены')
        return reverse_lazy('clients:detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(AdminRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    template_name = 'clients/confirm_delete.html'


class ClientSearchView(LoginRequiredMixin, View):
    def get(self, request):
        q = request.GET.get('q', '')
        qs = Client.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(phone__icontains=q)
        )
        if is_master(request.user):
            master = get_master_profile(request.user)
            if master:
                qs = qs.filter(appointments__master=master).distinct()
            else:
                qs = qs.none()
        clients = qs.values('id', 'first_name', 'last_name', 'phone')[:10]
        return JsonResponse(list(clients), safe=False)
