from django.db import models
from django.contrib.auth.models import User


class Role(models.TextChoices):
    ADMIN   = 'admin',   'Администратор'
    MANAGER = 'manager', 'Менеджер'
    MASTER  = 'master',  'Мастер'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.MANAGER,
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'
