"""
Formularios de la app projects.

ProjectForm  → crear/editar proyectos (ModelForm)
TaskForm     → crear/editar tareas (ModelForm)
"""

from django import forms
from .models import Project, Task


class ProjectForm(forms.ModelForm):
    """
    Formulario para crear y editar proyectos.
    Usa ModelForm para generar automáticamente los campos desde el modelo.
    """

    class Meta:
        model = Project
        # Excluimos 'owner' porque lo asignamos en la vista (= usuario autenticado)
        fields = ['name', 'description', 'status', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del proyecto (opcional)',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',   # Muestra el selector de fecha nativo del navegador
            }),
        }
        labels = {
            'name':        'Nombre',
            'description': 'Descripción',
            'status':      'Estado',
            'deadline':    'Fecha límite',
        }

    def clean_name(self):
        """Validación: el nombre no puede estar vacío ni tener solo espacios."""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('El nombre del proyecto no puede estar vacío.')
        return name


class TaskForm(forms.ModelForm):
    """
    Formulario para crear y editar tareas.
    El campo 'project' se asigna en la vista, no en el formulario.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la tarea',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción (opcional)',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'title':       'Título',
            'description': 'Descripción',
            'status':      'Estado',
            'priority':    'Prioridad',
            'due_date':    'Fecha límite',
        }

    def clean_title(self):
        """Validación: el título no puede tener solo espacios."""
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('El título de la tarea no puede estar vacío.')
        return title
