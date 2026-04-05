# TaskManager — 

Aplicación web desarrollada en **Django 5** que permite gestionar proyectos y tareas de forma eficiente, con sistema de autenticación de usuarios, panel de administración personalizado y cobertura de pruebas unitarias.

---

## Características

- Registro e inicio de sesión de usuarios (`django.contrib.auth`)
- Gestión completa de proyectos (crear, ver, editar, eliminar)
- Gestión de tareas con estados (Pendiente / En progreso / Completada) y prioridades
- Barra de progreso por proyecto
- Detección de tareas vencidas
- Protección CSRF en todos los formularios
- Restricción de acceso con `LoginRequiredMixin` (cada usuario solo ve sus datos)
- Admin de Django personalizado con inline de tareas dentro de proyectos
- Pruebas unitarias para modelos y vistas
- Interfaz responsiva con Bootstrap 5

---

## Requisitos

- Python 3.10 o superior
- pip

---

## Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/CarobethPaez/django-taskmanager.git
cd django-taskmanager
```

### 2. Crear y activar el entorno virtual

```bash
# En Linux / macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones (crea la base de datos SQLite)

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario para el panel de administración

```bash
python manage.py createsuperuser
```

Ingresa los datos que te pide (usuario, email, contraseña).

### 6. Levantar el servidor de desarrollo

```bash
python manage.py runserver
```

Abre el navegador en: **http://127.0.0.1:8000/**

---

## Uso de la aplicación

| URL | Descripción |
|-----|-------------|
| `/` | Redirige a la lista de proyectos |
| `/accounts/register/` | Registro de nuevo usuario |
| `/accounts/login/` | Inicio de sesión |
| `/accounts/logout/` | Cierre de sesión (POST) |
| `/accounts/profile/` | Perfil del usuario autenticado |
| `/projects/` | Lista de proyectos del usuario |
| `/projects/crear/` | Crear nuevo proyecto |
| `/projects/<id>/` | Detalle de un proyecto y sus tareas |
| `/projects/<id>/editar/` | Editar proyecto |
| `/projects/<id>/eliminar/` | Eliminar proyecto |
| `/projects/<id>/tareas/crear/` | Agregar tarea a un proyecto |
| `/projects/tareas/<id>/editar/` | Editar tarea |
| `/projects/tareas/<id>/eliminar/` | Eliminar tarea |
| `/admin/` | Panel de administración de Django |

---

## Estructura del proyecto

```
django-taskmanager/
│
├── manage.py                  # Comando principal de Django
├── requirements.txt           # Dependencias del proyecto
├── db.sqlite3                 # Base de datos (generada al migrar)
│
├── taskmanager/               # Configuración principal del proyecto
│   ├── settings.py            # Settings: BD, apps, auth, rutas de medios
│   ├── urls.py                # URLs raíz
│   └── wsgi.py
│
├── apps/
│   ├── accounts/              # App de autenticación
│   │   ├── forms.py           # RegisterForm, LoginForm
│   │   ├── views.py           # RegisterView, LoginView, LogoutView, ProfileView
│   │   ├── urls.py            # /accounts/...
│   │   ├── admin.py           # CustomUserAdmin
│   │   └── tests.py
│   │
│   └── projects/              # App de proyectos y tareas
│       ├── models.py          # Project, Task
│       ├── forms.py           # ProjectForm, TaskForm
│       ├── views.py           # CRUD de proyectos y tareas
│       ├── urls.py            # /projects/...
│       ├── admin.py           # ProjectAdmin, TaskAdmin con inline
│       └── tests.py           # 20+ pruebas unitarias
│
├── templates/                 # Templates HTML con herencia
│   ├── base.html              # Template padre (navbar, mensajes, footer)
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── projects/
│       ├── project_list.html
│       ├── project_detail.html
│       ├── project_form.html
│       ├── project_confirm_delete.html
│       ├── task_form.html
│       └── task_confirm_delete.html
│
└── static/
    ├── css/
    └── js/
```

---

## Ejecutar las pruebas unitarias

```bash
# Correr todos los tests
python manage.py test

# Correr solo los tests de proyectos con detalle
python manage.py test apps.projects --verbosity=2

# Correr solo los tests de accounts
python manage.py test apps.accounts --verbosity=2
```

---

## Decisiones técnicas destacadas

### Seguridad
- **CSRF**: todos los formularios incluyen `{% csrf_token %}` y Django valida el token en cada POST.
- **LoginRequiredMixin**: todas las vistas de proyectos y tareas requieren autenticación. Si el usuario no está logueado, es redirigido a `/accounts/login/`.
- **Ownership check**: las vistas filtran siempre por `owner=request.user` (o `project__owner=request.user`), por lo que un usuario nunca puede ver, editar ni eliminar datos de otro usuario.

### Modelos
- `Project` y `Task` usan `ForeignKey` con `on_delete=CASCADE`: borrar un proyecto borra todas sus tareas; borrar un usuario borra todos sus proyectos.
- Propiedades calculadas (`@property`) como `progress`, `task_count` e `is_overdue` mantienen la lógica de negocio dentro del modelo.

### Formularios
- Se usa `ModelForm` para generación automática de campos desde los modelos.
- Validaciones extras en `clean_name()` y `clean_email()` dentro de los formularios.
- Todos los widgets tienen clases Bootstrap aplicadas automáticamente.

---

## Tecnologías utilizadas

- **Django 5.1** — framework web
- **SQLite** — base de datos de desarrollo
- **Bootstrap 5** — framework CSS
- **Bootstrap Icons** — iconografía

---

## Licencia

MIT — libre para uso educativo y personal.
