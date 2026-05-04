from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Role


class UserCreateForm(forms.ModelForm):
    password  = forms.CharField(
        label='Пароль', widget=forms.PasswordInput,
        help_text='Минимум 8 символов'
    )
    role = forms.ChoiceField(
        label='Роль', choices=Role.choices
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
        return user


class UserEditForm(forms.ModelForm):
    role = forms.ChoiceField(label='Роль', choices=Role.choices)
    is_active = forms.BooleanField(label='Активен', required=False)

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
