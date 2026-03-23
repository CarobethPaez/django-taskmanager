"""
Formularios de la app accounts.

RegisterForm extiende UserCreationForm para agregar el campo email
y aplicar clases CSS de Bootstrap a todos los inputs.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Formulario de registro.
    Extiende el formulario base de Django agregando el campo email
    como obligatorio.
    """
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@ejemplo.com',
        })
    )

    class Meta:
        model = User
        # Campos que se mostrarán en el formulario
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos clases Bootstrap a todos los campos automáticamente
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Personalizamos los placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'

    def clean_email(self):
        """Validación extra: el email no puede estar ya registrado."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def save(self, commit=True):
        """Guardamos el email al crear el usuario."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Formulario de login.
    Extiende AuthenticationForm solo para aplicar estilos Bootstrap.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
        })
