from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Role


def get_user_role(user):
    """Return role string for the user. Superusers always get ADMIN."""
    if user.is_superuser:
        return Role.ADMIN
    try:
        return user.profile.role
    except Exception:
        return Role.MANAGER


def is_master(user):
    return get_user_role(user) == Role.MASTER


def is_manager_or_above(user):
    return get_user_role(user) in (Role.ADMIN, Role.MANAGER)


def is_admin(user):
    return get_user_role(user) == Role.ADMIN


def get_master_profile(user):
    """Return Master instance for user, or None."""
    try:
        return user.master_profile
    except Exception:
        return None


class RoleRequiredMixin(LoginRequiredMixin):
    """Restrict view to specific roles. Admin always passes."""
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        role = get_user_role(request.user)
        if role not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = [Role.ADMIN]


class ManagerRequiredMixin(RoleRequiredMixin):
    allowed_roles = [Role.ADMIN, Role.MANAGER]
