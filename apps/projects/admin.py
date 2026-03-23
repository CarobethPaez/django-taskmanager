"""
Configuración del admin para proyectos y tareas.
Registramos ambos modelos con vistas personalizadas.
"""

from django.contrib import admin
from .models import Project, Task


class TaskInline(admin.TabularInline):
    """
    Muestra las tareas de un proyecto directamente dentro
    del formulario de edición del proyecto (inline).
    """
    model = Task
    extra = 1   # Muestra 1 fila vacía por defecto para agregar tareas rápido
    fields = ('title', 'status', 'priority', 'due_date')
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin para el modelo Proyecto."""
    list_display  = ('name', 'owner', 'status', 'deadline', 'task_count', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('name', 'owner__username', 'description')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines       = [TaskInline]   # Tareas dentro del proyecto

    # Agrupamos los campos en secciones dentro del admin
    fieldsets = (
        ('Información principal', {
            'fields': ('name', 'owner', 'description')
        }),
        ('Estado y fechas', {
            'fields': ('status', 'deadline', 'created_at', 'updated_at')
        }),
    )

    def task_count(self, obj):
        return obj.task_count
    task_count.short_description = 'Tareas'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin para el modelo Tarea."""
    list_display  = ('title', 'project', 'status', 'priority', 'due_date', 'is_overdue')
    list_filter   = ('status', 'priority', 'project')
    search_fields = ('title', 'project__name', 'description')
    ordering      = ('status', '-priority')
    readonly_fields = ('created_at',)

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True   # Muestra un ícono de check/cruz en vez de True/False
    is_overdue.short_description = 'Vencida'
