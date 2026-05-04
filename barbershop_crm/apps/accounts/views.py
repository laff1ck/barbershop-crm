from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import UserProfile, Role
from .forms import UserCreateForm, UserEditForm, PasswordResetForm
from .mixins import AdminRequiredMixin, get_user_role


class UserListView(AdminRequiredMixin, ListView):
    template_name = 'accounts/users.html'
    context_object_name = 'users'

    def get_queryset(self):
        return (
            User.objects
            .select_related('profile', 'master_profile')
            .order_by('is_superuser', 'profile__role', 'username')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['role_choices'] = Role.choices
        ctx['role_counts']  = {
            'total':   User.objects.count(),
            'admin':   User.objects.filter(is_superuser=True).count(),
            'manager': UserProfile.objects.filter(role=Role.MANAGER).count(),
            'master':  UserProfile.objects.filter(role=Role.MASTER).count(),
        }
        return ctx


class UserCreateView(AdminRequiredMixin, CreateView):
    form_class    = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url   = reverse_lazy('accounts:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Пользователь «{self.object.username}» создан')
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Новый пользователь'
        return ctx


class UserEditView(AdminRequiredMixin, UpdateView):
    model         = User
    form_class    = UserEditForm
    template_name = 'accounts/user_form.html'
    success_url   = reverse_lazy('accounts:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Пользователь «{self.object.username}» обновлён')
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title']   = f'Редактировать: {self.object.username}'
        ctx['editing_user'] = self.object
        return ctx


class UserToggleActiveView(AdminRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            return JsonResponse({'error': 'Нельзя деактивировать себя'}, status=400)
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        return JsonResponse({'is_active': user.is_active})


class UserPasswordResetView(AdminRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        from django.shortcuts import render
        form = PasswordResetForm()
        return render(request, 'accounts/password_reset.html', {'form': form, 'target_user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Пароль для «{user.username}» изменён')
            return redirect('accounts:users')
        from django.shortcuts import render
        return render(request, 'accounts/password_reset.html', {'form': form, 'target_user': user})
