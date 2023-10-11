from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *

# dentro de settings.py configure el user_model por el personalizado que cree
User = get_user_model()

class FormularioRegistroUsuarioPersonalizado(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserEditForm(UserChangeForm):
    password= forms.CharField(
        help_text="",
        widget=forms.HiddenInput(), required = False
    )
    
    class Meta:
        model = UsuarioPersonalizado
        fields = ('email', 'first_name', 'last_name', 'imagen')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'label'}),
            'first_name': forms.TextInput(attrs={'class': 'label'}),
            'last_name': forms.TextInput(attrs={'class': 'label'}),
            'imagen': forms.FileInput(attrs={'class': 'label'}),
        }

class CrearDireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'barrio', 'ciudad', 'provincia', 'codigo_postal', 'comentarios']

class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'correo', 'mensaje']
        widgets = {
            'leido': forms.HiddenInput(),
        }

class InicioSesionForm(AuthenticationForm):
    model = UsuarioPersonalizado
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'label'})
        }