import uuid
from django.db import models


class PaymentMethod(models.TextChoices):
    CASH   = 'cash',   'Наличные'
    CARD   = 'card',   'Карта'
    ONLINE = 'online', 'Перевод'


class Payment(models.Model):
    appointment    = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.PROTECT,
        related_name='payment',
    )
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    method         = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    paid_at        = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=30, unique=True, blank=True)
    discount       = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text='Скидка в %'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f"Чек #{self.receipt_number} — {self.amount} ₽"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"RC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def final_amount(self):
        if self.discount:
            return self.amount * (1 - self.discount / 100)
        return self.amount

    @property
    def discount_amount(self):
        return self.amount - self.final_amount
