"""
Vistas de la app projects.

Todas las vistas usan LoginRequiredMixin → redirige a login si no está autenticado.

Proyectos:
  ProjectListView    → lista todos los proyectos del usuario
  ProjectCreateView  → crea un nuevo proyecto
  ProjectDetailView  → detalle de un proyecto + sus tareas
  ProjectUpdateView  → edita un proyecto existente
  ProjectDeleteView  → elimina un proyecto

Tareas:
  TaskCreateView  → crea una tarea en un proyecto
  TaskUpdateView  → edita una tarea existente
  TaskDeleteView  → elimina una tarea
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View

from .models import Project, Task
from .forms import ProjectForm, TaskForm


# ══════════════════════════════════════════════════════
#  VISTAS DE PROYECTOS
# ══════════════════════════════════════════════════════

class ProjectListView(LoginRequiredMixin, View):
    """
    Lista todos los proyectos que pertenecen al usuario autenticado.
    Filtramos por owner=request.user para que cada usuario vea solo los suyos.
    """
    template_name = 'projects/project_list.html'

    def get(self, request):
        projects = Project.objects.filter(owner=request.user)
        context = {
            'projects': projects,
            'total': projects.count(),
            'active': projects.filter(status=Project.STATUS_ACTIVE).count(),
            'finished': projects.filter(status=Project.STATUS_FINISHED).count(),
        }
        return render(request, self.template_name, context)


class ProjectCreateView(LoginRequiredMixin, View):
    """
    Crea un nuevo proyecto.
    El owner se asigna automáticamente al usuario autenticado.
    """
    template_name = 'projects/project_form.html'

    def get(self, request):
        form = ProjectForm()
        return render(request, self.template_name, {'form': form, 'action': 'Crear'})

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user   # Asignamos el dueño
            project.save()
            messages.success(request, f'Proyecto "{project.name}" creado exitosamente.')
            return redirect('projects:project_detail', pk=project.pk)
        messages.error(request, 'Por favor corregí los errores.')
        return render(request, self.template_name, {'form': form, 'action': 'Crear'})


class ProjectDetailView(LoginRequiredMixin, View):
    """
    Muestra el detalle de un proyecto y todas sus tareas.
    Verificamos que el proyecto pertenezca al usuario (owner=request.user).
    """
    template_name = 'projects/project_detail.html'

    def get(self, request, pk):
        # get_object_or_404 devuelve 404 si no existe o no le pertenece
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        tasks = project.task_set.all()
        context = {
            'project': project,
            'tasks': tasks,
            'todo_tasks':        tasks.filter(status=Task.STATUS_TODO),
            'progress_tasks':    tasks.filter(status=Task.STATUS_IN_PROGRESS),
            'done_tasks':        tasks.filter(status=Task.STATUS_DONE),
        }
        return render(request, self.template_name, context)


class ProjectUpdateView(LoginRequiredMixin, View):
    """Edita un proyecto existente."""
    template_name = 'projects/project_form.html'

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        form = ProjectForm(instance=project)
        return render(request, self.template_name, {
            'form': form, 'project': project, 'action': 'Editar'
        })

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Proyecto "{project.name}" actualizado.')
            return redirect('projects:project_detail', pk=project.pk)
        messages.error(request, 'Por favor corregí los errores.')
        return render(request, self.template_name, {
            'form': form, 'project': project, 'action': 'Editar'
        })


class ProjectDeleteView(LoginRequiredMixin, View):
    """
    Elimina un proyecto.
    GET  → muestra página de confirmación.
    POST → elimina el proyecto.
    """
    template_name = 'projects/project_confirm_delete.html'

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        return render(request, self.template_name, {'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        name = project.name
        project.delete()
        messages.success(request, f'Proyecto "{name}" eliminado.')
        return redirect('projects:project_list')


# ══════════════════════════════════════════════════════
#  VISTAS DE TAREAS
# ══════════════════════════════════════════════════════

class TaskCreateView(LoginRequiredMixin, View):
    """Crea una tarea dentro de un proyecto específico."""
    template_name = 'projects/task_form.html'

    def get(self, request, project_pk):
        project = get_object_or_404(Project, pk=project_pk, owner=request.user)
        form = TaskForm()
        return render(request, self.template_name, {
            'form': form, 'project': project, 'action': 'Crear'
        })

    def post(self, request, project_pk):
        project = get_object_or_404(Project, pk=project_pk, owner=request.user)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project   # Asignamos el proyecto
            task.save()
            messages.success(request, f'Tarea "{task.title}" creada.')
            return redirect('projects:project_detail', pk=project.pk)
        messages.error(request, 'Por favor corregí los errores.')
        return render(request, self.template_name, {
            'form': form, 'project': project, 'action': 'Crear'
        })


class TaskUpdateView(LoginRequiredMixin, View):
    """Edita una tarea existente."""
    template_name = 'projects/task_form.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        form = TaskForm(instance=task)
        return render(request, self.template_name, {
            'form': form, 'project': task.project, 'task': task, 'action': 'Editar'
        })

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tarea "{task.title}" actualizada.')
            return redirect('projects:project_detail', pk=task.project.pk)
        messages.error(request, 'Por favor corregí los errores.')
        return render(request, self.template_name, {
            'form': form, 'project': task.project, 'task': task, 'action': 'Editar'
        })


class TaskDeleteView(LoginRequiredMixin, View):
    """Elimina una tarea."""
    template_name = 'projects/task_confirm_delete.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        return render(request, self.template_name, {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        project_pk = task.project.pk
        title = task.title
        task.delete()
        messages.success(request, f'Tarea "{title}" eliminada.')
        return redirect('projects:project_detail', pk=project_pk)
