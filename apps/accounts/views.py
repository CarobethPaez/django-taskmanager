"""
Vistas de la app accounts.

- RegisterView  → registro de nuevos usuarios
- LoginView     → inicio de sesión (usa la vista de Django con form propio)
- LogoutView    → cierre de sesión
- ProfileView   → perfil del usuario autenticado (protegida con LoginRequiredMixin)
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages

from .forms import RegisterForm, LoginForm


class RegisterView(View):
    """
    Vista de registro.
    GET  → muestra el formulario vacío.
    POST → valida los datos y crea el usuario; luego lo loguea y redirige.
    """
    template_name = 'accounts/register.html'

    def get(self, request):
        # Si el usuario ya está autenticado, lo redirigimos directamente
        if request.user.is_authenticated:
            return redirect('projects:project_list')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Logueamos automáticamente al usuario recién registrado
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada exitosamente.')
            return redirect('projects:project_list')
        # Si el formulario tiene errores, los mostramos
        messages.error(request, 'Por favor corregí los errores del formulario.')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(View):
    """
    Vista de login personalizada.
    GET  → muestra el formulario.
    POST → autentica al usuario y redirige según LOGIN_REDIRECT_URL.
    """
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('projects:project_list')
        form = LoginForm(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Hola de nuevo, {user.username}!')
            # Respetamos el parámetro "next" si existe (Django lo usa internamente)
            next_url = request.GET.get('next', 'projects:project_list')
            return redirect(next_url)
        messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, self.template_name, {'form': form})


class CustomLogoutView(View):
    """
    Vista de logout.
    Solo acepta POST para evitar cerrar sesión por GET (buena práctica de seguridad).
    """
    def post(self, request):
        logout(request)
        messages.info(request, 'Cerraste sesión correctamente.')
        return redirect('accounts:login')


class ProfileView(LoginRequiredMixin, View):
    """
    Perfil del usuario.
    LoginRequiredMixin redirige automáticamente a LOGIN_URL si no está autenticado.
    """
    template_name = 'accounts/profile.html'

    def get(self, request):
        # Pasamos estadísticas básicas al template
        context = {
            'total_projects': request.user.project_set.count(),
            'total_tasks': sum(p.task_set.count() for p in request.user.project_set.all()),
        }
        return render(request, self.template_name, context)
