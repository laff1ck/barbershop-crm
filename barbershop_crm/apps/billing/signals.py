from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Payment
from apps.appointments.models import Appointment, AppointmentStatus


@receiver(post_save, sender=Payment)
def on_payment_created(sender, instance, created, **kwargs):
    if not created:
        return

    appt = instance.appointment
    client = appt.client

    # Update appointment status to done
    appt.status = AppointmentStatus.DONE
    appt.price_paid = instance.final_amount
    appt.save(update_fields=['status', 'price_paid', 'updated_at'])

    # Update client stats
    client.total_spent = float(client.total_spent) + float(instance.final_amount)
    client.visit_count += 1
    client.last_visit = timezone.localdate()
    client.save(update_fields=['total_spent', 'visit_count', 'last_visit'])

    # Recalculate loyalty tier
    client.recalculate_tier()
