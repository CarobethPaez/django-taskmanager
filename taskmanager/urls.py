"""
URLs raíz del proyecto TaskManager.

Estructura de rutas:
  /                  → redirige al dashboard de proyectos
  /accounts/         → registro, login, logout
  /projects/         → gestión de proyectos y tareas
  /admin/            → panel de administración de Django
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # Redirige la raíz "/" al listado de proyectos
    path('', RedirectView.as_view(url='/projects/', permanent=False)),

    # Rutas de autenticación (registro, login, logout)
    path('accounts/', include('apps.accounts.urls')),

    # Rutas de proyectos y tareas
    path('projects/', include('apps.projects.urls')),
]

# Servir archivos de medios en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
