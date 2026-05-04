from datetime import timedelta
from django.db import models
from django.utils import timezone


class AppointmentStatus(models.TextChoices):
    PENDING     = 'pending',     'Ожидает'
    CONFIRMED   = 'confirmed',   'Подтверждён'
    IN_PROGRESS = 'in_progress', 'В процессе'
    DONE        = 'done',        'Завершён'
    CANCELLED   = 'cancelled',   'Отменён'
    NO_SHOW     = 'no_show',     'Не явился'


STATUS_COLOR_MAP = {
    AppointmentStatus.PENDING:     '#6c757d',
    AppointmentStatus.CONFIRMED:   '#c9a84c',
    AppointmentStatus.IN_PROGRESS: '#0dcaf0',
    AppointmentStatus.DONE:        '#198754',
    AppointmentStatus.CANCELLED:   '#dc3545',
    AppointmentStatus.NO_SHOW:     '#6f42c1',
}

STATUS_BADGE_MAP = {
    AppointmentStatus.PENDING:     'secondary',
    AppointmentStatus.CONFIRMED:   'warning',
    AppointmentStatus.IN_PROGRESS: 'info',
    AppointmentStatus.DONE:        'success',
    AppointmentStatus.CANCELLED:   'danger',
    AppointmentStatus.NO_SHOW:     'purple',
}


class Appointment(models.Model):
    client  = models.ForeignKey(
        'clients.Client', on_delete=models.PROTECT, related_name='appointments'
    )
    master  = models.ForeignKey(
        'staff.Master', on_delete=models.PROTECT, related_name='appointments'
    )
    service = models.ForeignKey(
        'services.Service', on_delete=models.PROTECT, related_name='appointments'
    )

    start_time = models.DateTimeField()
    end_time   = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
        db_index=True,
    )

    price_paid  = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(
        'auth.User', null=True, on_delete=models.SET_NULL,
        related_name='created_appointments'
    )

    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['start_time', 'master']),
            models.Index(fields=['status', 'start_time']),
            models.Index(fields=['client', 'start_time']),
        ]

    def __str__(self):
        return (
            f"{self.client} → {self.master} | "
            f"{self.start_time:%d.%m %H:%M} [{self.get_status_display()}]"
        )

    def save(self, *args, **kwargs):
        if self.service_id and not self.end_time:
            self.end_time = self.start_time + timedelta(minutes=self.service.duration)
        super().save(*args, **kwargs)

    @property
    def status_color(self):
        return STATUS_COLOR_MAP.get(self.status, '#c9a84c')

    @property
    def status_badge(self):
        return STATUS_BADGE_MAP.get(self.status, 'secondary')

    def to_fullcalendar_event(self):
        return {
            'id':    self.pk,
            'title': f"{self.client.full_name} — {self.service.name}",
            'start': self.start_time.isoformat(),
            'end':   self.end_time.isoformat() if self.end_time else None,
            'resourceId': str(self.master_id),
            'color': STATUS_COLOR_MAP.get(self.status, '#c9a84c'),
            'extendedProps': {
                'status':    self.status,
                'statusLabel': self.get_status_display(),
                'client_id': self.client_id,
                'master_id': self.master_id,
                'service':   self.service.name,
                'phone':     self.client.phone,
                'notes':     self.notes,
                'price':     str(self.price_paid or self.service.price),
            },
        }
