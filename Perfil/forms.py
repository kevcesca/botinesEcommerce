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
    
    def __init__(self, *args, **kwargs):
        super(FormularioRegistroUsuarioPersonalizado, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'label '})
        self.fields['email'].widget.attrs.update({'class': 'label '})
        self.fields['password1'].widget.attrs.update({'class': 'label '})
        self.fields['password2'].widget.attrs.update({'class': 'label '})

        # Configuración de help_text vacío
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

class UserEditForm(forms.ModelForm):
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
    def __init__(self, *args, **kwargs):
        super(CrearDireccionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'label'

    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'barrio', 'ciudad', 'provincia', 'codigo_postal', 'comentarios']

class MensajeContactoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MensajeContactoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'label'
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


