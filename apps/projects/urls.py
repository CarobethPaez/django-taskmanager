"""
URLs de la app projects.

  /projects/                        → lista de proyectos
  /projects/crear/                  → crear proyecto
  /projects/<pk>/                   → detalle del proyecto
  /projects/<pk>/editar/            → editar proyecto
  /projects/<pk>/eliminar/          → eliminar proyecto
  /projects/<pk>/tareas/crear/      → crear tarea en un proyecto
  /projects/tareas/<pk>/editar/     → editar tarea
  /projects/tareas/<pk>/eliminar/   → eliminar tarea
"""

from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # ── Proyectos ──────────────────────────────────────────────────
    path('',                    views.ProjectListView.as_view(),   name='project_list'),
    path('crear/',              views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/',           views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/editar/',    views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/eliminar/',  views.ProjectDeleteView.as_view(), name='project_delete'),

    # ── Tareas ─────────────────────────────────────────────────────
    path('<int:project_pk>/tareas/crear/',   views.TaskCreateView.as_view(), name='task_create'),
    path('tareas/<int:pk>/editar/',          views.TaskUpdateView.as_view(), name='task_update'),
    path('tareas/<int:pk>/eliminar/',        views.TaskDeleteView.as_view(), name='task_delete'),
]
