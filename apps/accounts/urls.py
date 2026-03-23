"""
URLs de la app accounts.

  /accounts/register/  → registro de nuevos usuarios
  /accounts/login/     → inicio de sesión
  /accounts/logout/    → cierre de sesión (POST)
  /accounts/profile/   → perfil del usuario autenticado
"""

from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView

app_name = 'accounts'   # Namespace para usar en templates como {% url 'accounts:login' %}

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    CustomLoginView.as_view(), name='login'),
    path('logout/',   CustomLogoutView.as_view(), name='logout'),
    path('profile/',  ProfileView.as_view(), name='profile'),
]
