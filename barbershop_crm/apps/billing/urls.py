from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('create/<int:appt_pk>/', views.PaymentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='detail'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('reports/export/', views.ExportCSVView.as_view(), name='export'),
]
