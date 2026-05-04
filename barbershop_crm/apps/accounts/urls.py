from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',               views.UserListView.as_view(),          name='users'),
    path('create/',        views.UserCreateView.as_view(),         name='user_create'),
    path('<int:pk>/edit/', views.UserEditView.as_view(),           name='user_edit'),
    path('<int:pk>/toggle/', views.UserToggleActiveView.as_view(), name='user_toggle'),
    path('<int:pk>/password/', views.UserPasswordResetView.as_view(), name='user_password'),
]
