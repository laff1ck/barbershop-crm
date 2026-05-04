from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='list'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('create/', views.AppointmentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='edit'),
    # JSON API
    path('api/events/', views.AppointmentEventsAPIView.as_view(), name='api_events'),
    path('api/<int:pk>/status/', views.AppointmentStatusAPIView.as_view(), name='api_status'),
    path('api/<int:pk>/move/', views.AppointmentMoveAPIView.as_view(), name='api_move'),
]
