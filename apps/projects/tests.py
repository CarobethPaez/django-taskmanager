"""
Pruebas unitarias para la app projects.

Cubren:
  - Modelos: Project y Task (creación, propiedades calculadas, relaciones)
  - Vistas: autenticación requerida, CRUD de proyectos y tareas
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime

from .models import Project, Task


# ══════════════════════════════════════════════════════════════
#  TESTS DE MODELOS
# ══════════════════════════════════════════════════════════════

class ProjectModelTest(TestCase):
    """Pruebas para el modelo Project."""

    def setUp(self):
        """Se ejecuta antes de cada test. Crea datos de base."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@ejemplo.com'
        )
        self.project = Project.objects.create(
            owner=self.user,
            name='Proyecto de prueba',
            description='Descripción de prueba',
            status=Project.STATUS_ACTIVE,
        )

    def test_project_creation(self):
        """El proyecto se crea correctamente con los datos dados."""
        self.assertEqual(self.project.name, 'Proyecto de prueba')
        self.assertEqual(self.project.owner, self.user)
        self.assertEqual(self.project.status, Project.STATUS_ACTIVE)

    def test_project_str(self):
        """El método __str__ devuelve el formato esperado."""
        expected = f'Proyecto de prueba ({self.user.username})'
        self.assertEqual(str(self.project), expected)

    def test_task_count_empty(self):
        """Un proyecto sin tareas devuelve 0."""
        self.assertEqual(self.project.task_count, 0)

    def test_task_count_with_tasks(self):
        """task_count refleja la cantidad real de tareas."""
        Task.objects.create(project=self.project, title='Tarea 1')
        Task.objects.create(project=self.project, title='Tarea 2')
        self.assertEqual(self.project.task_count, 2)

    def test_progress_no_tasks(self):
        """El progreso es 0 cuando no hay tareas."""
        self.assertEqual(self.project.progress, 0)

    def test_progress_with_completed_tasks(self):
        """El progreso calcula correctamente el porcentaje."""
        Task.objects.create(project=self.project, title='T1', status=Task.STATUS_DONE)
        Task.objects.create(project=self.project, title='T2', status=Task.STATUS_TODO)
        # 1 de 2 completadas = 50%
        self.assertEqual(self.project.progress, 50)

    def test_project_ordering(self):
        """Los proyectos se ordenan del más nuevo al más viejo."""
        project2 = Project.objects.create(owner=self.user, name='Proyecto 2')
        projects = Project.objects.filter(owner=self.user)
        # El primero en el queryset debe ser el más reciente
        self.assertEqual(projects[0], project2)


class TaskModelTest(TestCase):
    """Pruebas para el modelo Task."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='pass123')
        self.project = Project.objects.create(owner=self.user, name='Proyecto')
        self.task = Task.objects.create(
            project=self.project,
            title='Tarea de prueba',
            status=Task.STATUS_TODO,
            priority=Task.PRIORITY_HIGH,
        )

    def test_task_creation(self):
        """La tarea se crea con los campos correctos."""
        self.assertEqual(self.task.title, 'Tarea de prueba')
        self.assertEqual(self.task.status, Task.STATUS_TODO)
        self.assertEqual(self.task.priority, Task.PRIORITY_HIGH)

    def test_task_str(self):
        """__str__ muestra el título y estado."""
        self.assertIn('Tarea de prueba', str(self.task))

    def test_task_is_not_overdue_without_due_date(self):
        """Sin fecha límite, is_overdue debe ser False."""
        self.assertFalse(self.task.is_overdue)

    def test_task_is_overdue(self):
        """Una tarea con fecha pasada y no completada es overdue."""
        self.task.due_date = datetime.date(2020, 1, 1)  # Fecha pasada
        self.task.save()
        self.assertTrue(self.task.is_overdue)

    def test_task_done_is_not_overdue(self):
        """Una tarea completada no es overdue aunque la fecha pasó."""
        self.task.due_date = datetime.date(2020, 1, 1)
        self.task.status = Task.STATUS_DONE
        self.task.save()
        self.assertFalse(self.task.is_overdue)

    def test_cascade_delete(self):
        """Al borrar el proyecto, se borran sus tareas."""
        task_pk = self.task.pk
        self.project.delete()
        self.assertFalse(Task.objects.filter(pk=task_pk).exists())


# ══════════════════════════════════════════════════════════════
#  TESTS DE VISTAS
# ══════════════════════════════════════════════════════════════

class ProjectViewsTest(TestCase):
    """Pruebas para las vistas de proyectos."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='pass123')
        self.other_user = User.objects.create_user(username='other', password='pass456')

        self.project = Project.objects.create(
            owner=self.user,
            name='Proyecto de vista',
        )

    # ── Autenticación requerida ─────────────────────────────────

    def test_project_list_requires_login(self):
        """Sin login, redirige al login."""
        response = self.client.get(reverse('projects:project_list'))
        self.assertRedirects(response, '/accounts/login/?next=/projects/')

    def test_project_detail_requires_login(self):
        """El detalle también exige autenticación."""
        url = reverse('projects:project_detail', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # ── Vistas autenticadas ─────────────────────────────────────

    def test_project_list_authenticated(self):
        """Un usuario autenticado ve su lista de proyectos."""
        self.client.login(username='viewuser', password='pass123')
        response = self.client.get(reverse('projects:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Proyecto de vista')

    def test_project_list_shows_only_own_projects(self):
        """El usuario solo ve sus propios proyectos."""
        Project.objects.create(owner=self.other_user, name='Proyecto ajeno')
        self.client.login(username='viewuser', password='pass123')
        response = self.client.get(reverse('projects:project_list'))
        self.assertContains(response, 'Proyecto de vista')
        self.assertNotContains(response, 'Proyecto ajeno')

    def test_create_project_get(self):
        """GET al formulario de creación devuelve 200."""
        self.client.login(username='viewuser', password='pass123')
        response = self.client.get(reverse('projects:project_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_project_post_valid(self):
        """POST con datos válidos crea el proyecto y redirige."""
        self.client.login(username='viewuser', password='pass123')
        response = self.client.post(reverse('projects:project_create'), {
            'name': 'Nuevo Proyecto',
            'description': 'Descripción',
            'status': 'active',
        })
        self.assertEqual(Project.objects.filter(name='Nuevo Proyecto').count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_create_project_post_invalid(self):
        """POST sin nombre no crea el proyecto y vuelve al formulario."""
        self.client.login(username='viewuser', password='pass123')
        response = self.client.post(reverse('projects:project_create'), {
            'name': '',   # Campo obligatorio vacío
            'status': 'active',
        })
        self.assertEqual(response.status_code, 200)  # Vuelve al formulario
        self.assertFalse(Project.objects.filter(name='').exists())

    def test_project_detail_own(self):
        """El dueño puede ver el detalle de su proyecto."""
        self.client.login(username='viewuser', password='pass123')
        url = reverse('projects:project_detail', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Proyecto de vista')

    def test_project_detail_other_user_gets_404(self):
        """Otro usuario no puede ver un proyecto ajeno."""
        self.client.login(username='other', password='pass456')
        url = reverse('projects:project_detail', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_project(self):
        """El dueño puede eliminar su propio proyecto."""
        self.client.login(username='viewuser', password='pass123')
        url = reverse('projects:project_delete', args=[self.project.pk])
        response = self.client.post(url)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertEqual(response.status_code, 302)


class TaskViewsTest(TestCase):
    """Pruebas para las vistas de tareas."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='taskuser', password='pass123')
        self.project = Project.objects.create(owner=self.user, name='Proyecto')
        self.task = Task.objects.create(
            project=self.project,
            title='Tarea existente',
            status=Task.STATUS_TODO,
        )

    def test_create_task_post_valid(self):
        """POST con datos válidos crea la tarea."""
        self.client.login(username='taskuser', password='pass123')
        url = reverse('projects:task_create', args=[self.project.pk])
        response = self.client.post(url, {
            'title': 'Nueva tarea',
            'status': 'todo',
            'priority': 'medium',
        })
        self.assertTrue(Task.objects.filter(title='Nueva tarea').exists())
        self.assertEqual(response.status_code, 302)

    def test_update_task(self):
        """Se puede actualizar el estado de una tarea."""
        self.client.login(username='taskuser', password='pass123')
        url = reverse('projects:task_update', args=[self.task.pk])
        self.client.post(url, {
            'title': 'Tarea existente',
            'status': Task.STATUS_DONE,
            'priority': 'medium',
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.STATUS_DONE)

    def test_delete_task(self):
        """El dueño puede eliminar una tarea."""
        self.client.login(username='taskuser', password='pass123')
        url = reverse('projects:task_delete', args=[self.task.pk])
        self.client.post(url)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


# ══════════════════════════════════════════════════════════════
#  TESTS DE AUTENTICACIÓN
# ══════════════════════════════════════════════════════════════

class AccountsTest(TestCase):
    """Pruebas para registro y login."""

    def setUp(self):
        self.client = Client()

    def test_register_get(self):
        """GET al registro devuelve 200."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post_valid(self):
        """POST con datos válidos crea el usuario."""
        response = self.client.post(reverse('accounts:register'), {
            'username':  'newuser',
            'email':     'new@ejemplo.com',
            'password1': 'SuperPass123!',
            'password2': 'SuperPass123!',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.status_code, 302)

    def test_register_duplicate_email(self):
        """No se puede registrar un email ya usado."""
        User.objects.create_user(username='existing', email='dup@ejemplo.com', password='pass123')
        response = self.client.post(reverse('accounts:register'), {
            'username':  'newuser2',
            'email':     'dup@ejemplo.com',   # Email duplicado
            'password1': 'SuperPass123!',
            'password2': 'SuperPass123!',
        })
        self.assertEqual(response.status_code, 200)   # Vuelve al form con error
        self.assertEqual(User.objects.filter(email='dup@ejemplo.com').count(), 1)

    def test_login_valid(self):
        """Login con credenciales correctas redirige al dashboard."""
        User.objects.create_user(username='loginuser', password='pass123')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'loginuser',
            'password': 'pass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid(self):
        """Login con contraseña incorrecta vuelve al formulario."""
        User.objects.create_user(username='loginuser2', password='correct')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'loginuser2',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
