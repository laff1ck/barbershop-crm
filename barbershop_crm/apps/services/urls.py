from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('create/', views.ServiceCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='edit'),
    path('<int:pk>/toggle/', views.ServiceToggleView.as_view(), name='toggle'),
]
