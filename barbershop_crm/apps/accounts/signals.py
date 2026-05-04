from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Role


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create UserProfile for new non-superuser accounts."""
    if created and not instance.is_superuser:
        role = Role.MASTER if hasattr(instance, 'master_profile') else Role.MANAGER
        UserProfile.objects.get_or_create(user=instance, defaults={'role': role})
