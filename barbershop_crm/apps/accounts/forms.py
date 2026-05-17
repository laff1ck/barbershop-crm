from datetime import time
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Role


def _setup_new_master(master):
    """Assign all active services and default work schedule (Mon–Sat 10:00–20:00) to a new master."""
    from apps.services.models import Service
    from apps.staff.models import WorkSchedule
    master.services.set(Service.objects.filter(is_active=True))
    # Mon=0 … Sat=5 work days, Sun=6 day off
    for weekday in range(7):
        WorkSchedule.objects.get_or_create(
            master=master,
            weekday=weekday,
            defaults={
                'start_time': time(10, 0),
                'end_time':   time(20, 0),
                'is_day_off': weekday == 6,  # Sunday off
            }
        )


class UserCreateForm(forms.ModelForm):
    password  = forms.CharField(
        label='Пароль', widget=forms.PasswordInput,
        help_text='Минимум 8 символов'
    )
    role = forms.ChoiceField(
        label='Роль', choices=Role.choices
    )
    master_profile = forms.IntegerField(
        label='Профиль мастера',
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username':   'Логин',
            'first_name': 'Имя',
            'last_name':  'Фамилия',
            'email':      'Email',
        }

    def clean_password(self):
        pw = self.cleaned_data.get('password')
        validate_password(pw)
        return pw

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'role': self.cleaned_data['role']}
            )
            if self.cleaned_data.get('role') == Role.MASTER:
                from apps.staff.models import Master
                master_pk = self.cleaned_data.get('master_profile')
                if master_pk:
                    # Link existing master profile
                    try:
                        master = Master.objects.get(pk=master_pk)
                        master.user = user
                        master.save(update_fields=['user'])
                    except Master.DoesNotExist:
                        pass
                else:
                    # Auto-create master profile so user appears on booking page
                    display_name = (
                        f"{user.first_name} {user.last_name}".strip()
                        or user.username
                    )
                    master = Master.objects.create(user=user, display_name=display_name)
                    _setup_new_master(master)
        return user


class UserEditForm(forms.ModelForm):
    role      = forms.ChoiceField(label='Роль', choices=Role.choices)
    is_active = forms.BooleanField(label='Активен', required=False)
    master_profile = forms.IntegerField(
        label='Профиль мастера',
        required=False,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'is_active']
        labels = {
            'first_name': 'Имя',
            'last_name':  'Фамилия',
            'email':      'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['role'].initial = self.instance.profile.role

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'role': self.cleaned_data['role']}
            )
            if self.cleaned_data.get('role') == Role.MASTER:
                from apps.staff.models import Master
                master_pk = self.cleaned_data.get('master_profile')
                if master_pk:
                    # Link existing master profile
                    try:
                        master = Master.objects.get(pk=master_pk)
                        master.user = user
                        master.save(update_fields=['user'])
                    except Master.DoesNotExist:
                        pass
                else:
                    # Auto-create master profile if user doesn't have one yet
                    if not Master.objects.filter(user=user).exists():
                        display_name = (
                            f"{user.first_name} {user.last_name}".strip()
                            or user.username
                        )
                        master = Master.objects.create(user=user, display_name=display_name)
                        _setup_new_master(master)
        return user


class PasswordResetForm(forms.Form):
    password  = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают')
        validate_password(cd.get('password'))
        return cd
