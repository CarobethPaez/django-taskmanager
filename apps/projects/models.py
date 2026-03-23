"""
Modelos de la app projects.

Proyecto  → pertenece a un usuario (ForeignKey a User).
Tarea     → pertenece a un proyecto (ForeignKey a Proyecto).

Relación:
  User  1──N  Proyecto  1──N  Tarea
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    """
    Modelo que representa un proyecto de trabajo.

    Campos:
      owner       → usuario dueño del proyecto (ForeignKey)
      name        → nombre del proyecto
      description → descripción opcional
      created_at  → fecha de creación (automática)
      updated_at  → última actualización (automática)
    """

    # Opciones de estado del proyecto
    STATUS_ACTIVE   = 'active'
    STATUS_PAUSED   = 'paused'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = [
        (STATUS_ACTIVE,   'Activo'),
        (STATUS_PAUSED,   'Pausado'),
        (STATUS_FINISHED, 'Finalizado'),
    ]

    # ── Relación con el usuario ─────────────────────────────────────────────
    # on_delete=CASCADE: si se borra el usuario, se borran sus proyectos
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_set',   # user.project_set.all()
        verbose_name='Propietario',
    )

    # ── Campos del proyecto ─────────────────────────────────────────────────
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre del proyecto',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        verbose_name='Estado',
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha límite',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True,     verbose_name='Actualizado el')

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-created_at']   # Los más nuevos primero

    def __str__(self):
        return f'{self.name} ({self.owner.username})'

    @property
    def task_count(self):
        """Cantidad total de tareas del proyecto."""
        return self.task_set.count()

    @property
    def completed_task_count(self):
        """Cantidad de tareas completadas."""
        return self.task_set.filter(status=Task.STATUS_DONE).count()

    @property
    def progress(self):
        """Porcentaje de tareas completadas (0-100)."""
        total = self.task_count
        if total == 0:
            return 0
        return int((self.completed_task_count / total) * 100)


class Task(models.Model):
    """
    Modelo que representa una tarea dentro de un proyecto.

    Campos:
      project     → proyecto al que pertenece (ForeignKey)
      title       → título de la tarea
      description → descripción opcional
      status      → pendiente / en progreso / completada
      priority    → baja / media / alta
      due_date    → fecha de vencimiento (opcional)
      created_at  → fecha de creación (automática)
    """

    # ── Opciones de estado ──────────────────────────────────────────────────
    STATUS_TODO       = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE       = 'done'

    STATUS_CHOICES = [
        (STATUS_TODO,        'Pendiente'),
        (STATUS_IN_PROGRESS, 'En progreso'),
        (STATUS_DONE,        'Completada'),
    ]

    # ── Opciones de prioridad ───────────────────────────────────────────────
    PRIORITY_LOW    = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH   = 'high'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW,    'Baja'),
        (PRIORITY_MEDIUM, 'Media'),
        (PRIORITY_HIGH,   'Alta'),
    ]

    # ── Relación con el proyecto ────────────────────────────────────────────
    # Si se borra el proyecto, se borran todas sus tareas
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='task_set',   # project.task_set.all()
        verbose_name='Proyecto',
    )

    # ── Campos de la tarea ──────────────────────────────────────────────────
    title = models.CharField(
        max_length=300,
        verbose_name='Título',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO,
        verbose_name='Estado',
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
        verbose_name='Prioridad',
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha límite',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['status', '-priority', 'due_date']

    def __str__(self):
        return f'{self.title} [{self.get_status_display()}]'

    @property
    def is_overdue(self):
        """Retorna True si la tarea venció y no está completada."""
        if self.due_date and self.status != self.STATUS_DONE:
            return self.due_date < timezone.now().date()
        return False
