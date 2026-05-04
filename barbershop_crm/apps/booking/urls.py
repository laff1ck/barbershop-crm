from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('',                              views.BookingPageView.as_view(),   name='page'),
    path('api/masters/',                  views.MastersAPIView.as_view(),    name='api_masters'),
    path('api/masters/<int:master_id>/services/', views.ServicesAPIView.as_view(), name='api_services'),
    path('api/masters/<int:master_id>/slots/',    views.SlotsAPIView.as_view(),    name='api_slots'),
    path('api/submit/',                   views.BookingSubmitView.as_view(), name='api_submit'),
]
