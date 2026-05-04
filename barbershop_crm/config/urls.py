from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# Restrict Django Admin to superusers only
class SuperuserAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


admin.site.__class__ = SuperuserAdminSite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.core.urls')),
    path('clients/', include('apps.clients.urls')),
    path('staff/', include('apps.staff.urls')),
    path('services/', include('apps.services.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('billing/', include('apps.billing.urls')),
    path('settings/', include('apps.accounts.urls')),
    path('book/', include('apps.booking.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
