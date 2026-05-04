from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.MasterListView.as_view(), name='list'),
    path('create/', views.MasterCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MasterDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.MasterUpdateView.as_view(), name='edit'),
]
