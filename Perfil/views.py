from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import *
from .forms import *
from Tienda.models import Pedido

# Create your views here.

def loginView(req):
    
    if req.method == "POST":
        miFormulario = InicioSesionForm(req, data = req.POST)
        
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            usuario = data ["username"]
            psw = data ["password"]
        
            user = authenticate(username = usuario, password = psw)
            
            if user:
                login(req, user)
                messages.success(req, f"Bienvenido {usuario}")
                return redirect("Inicio")
            else:
                messages.success(req, "Datos incorrectos")
                return redirect("Inicio")
        else:
            messages.success(req, "Formulario invalido")
            return redirect("Inicio")
    
    else:
        miFormulario = InicioSesionForm()
        return render(req, "login.html", {"miFormulario": miFormulario})


def registerView(request):
    if request.method == 'POST':
        form = FormularioRegistroUsuarioPersonalizado(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"Bienvenido {username}. Tu cuenta ha sido creada exitosamente.")
            return redirect('Inicio')
        else:
            messages.error(request, 'Ha ocurrido un error al crear tu cuenta. Por favor, intenta de nuevo.')
    else:
        form = FormularioRegistroUsuarioPersonalizado()
    return render(request, 'register.html', {'form': form})


class PerfilUsuarioView(LoginRequiredMixin, DetailView):
    model = UsuarioPersonalizado
    template_name = 'perfilUsuario.html'  

    def get_object(self):
        return self.request.user  # Obtiene el usuario logeado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['direcciones'] = user.direcciones.all()  # Obtiene las direcciones vinculadas al usuario
        return context


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('Perfil')  
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'editarPerfil.html', {'form': form})


@login_required
def crear_direccion(request):
    if request.method == 'POST':
        form = CrearDireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.usuario = request.user  # Asigna el usuario actual como propietario de la dirección
            direccion.save()
            messages.success(request, 'Direccion creada con éxito')
            return redirect('Perfil')  
    else:
        form = CrearDireccionForm()
    
    return render(request, 'crearDireccion.html', {'form': form})


@login_required
def editar_direccion(request, direccion_id):
    direccion = get_object_or_404(Direccion, id=direccion_id, usuario=request.user)

    if request.method == 'POST':
        form = CrearDireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            return redirect('Perfil') 
    else:
        form = CrearDireccionForm(instance=direccion)
    
    return render(request, 'editarDireccion.html', {'form': form})


@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Verificar si la contraseña actual es correcta
            user = form.user
            old_password = form.cleaned_data['old_password']
            if user.check_password(old_password):
                # Cambiar la contraseña y actualizar la sesión de autenticación
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
                return redirect('Perfil')  # Cambia 'perfil_usuario' al nombre de tu vista de perfil
            else:
                messages.error(request, 'La contraseña actual es incorrecta.')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'cambiarPassword.html', {'form': form})


@login_required
def pedidos_usuario(request):
    usuario = request.user
    pedidos = Pedido.objects.filter(cliente=usuario)
    return render(request, 'pedidosUsuario.html', {'pedidos': pedidos})


def contactanos(request):
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            mensaje_contacto = form.save(commit=False)
            mensaje_contacto.leido = False  # El mensaje se marca como no leído por defecto
            mensaje_contacto.save()
            # Puedes agregar aquí una lógica para notificar al administrador sobre el mensaje.
            return redirect('Contactanos2')
    else:
        form = MensajeContactoForm()
    
    return render(request, 'contactanos.html', {'form': form})


def contactanosGracias(request):
    return render(request, 'contactanos2.html')


@staff_member_required
def mensajesContactanos(request):
    mensajes_contactanos = MensajeContacto.objects.all()
    return render(request, 'mensajesContacto.html', {'mensajes_contactanos': mensajes_contactanos})