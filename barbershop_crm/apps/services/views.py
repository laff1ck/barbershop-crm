from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Service, ServiceCategory
from .forms import ServiceForm
from apps.accounts.mixins import AdminRequiredMixin


class ServiceListView(LoginRequiredMixin, ListView):
    model = ServiceCategory
    template_name = 'services/list.html'
    context_object_name = 'categories'
    queryset = ServiceCategory.objects.prefetch_related('services')


class ServiceCreateView(AdminRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/form.html'
    success_url = reverse_lazy('services:list')

    def form_valid(self, form):
        messages.success(self.request, 'Услуга добавлена')
        return super().form_valid(form)


class ServiceUpdateView(AdminRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/form.html'
    success_url = reverse_lazy('services:list')

    def form_valid(self, form):
        messages.success(self.request, 'Услуга обновлена')
        return super().form_valid(form)


class ServiceToggleView(AdminRequiredMixin, View):
    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        service.is_active = not service.is_active
        service.save(update_fields=['is_active'])
        return JsonResponse({'active': service.is_active})
