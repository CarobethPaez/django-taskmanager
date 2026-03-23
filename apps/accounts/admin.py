"""
Configuración del admin para la app accounts.
Extendemos UserAdmin para mostrar columnas extra en el listado de usuarios.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Primero desregistramos el UserAdmin por defecto
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin personalizado para User.
    Muestra email, estado de staff y fecha de ingreso en la lista.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter  = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
