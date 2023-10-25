from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from Perfil.views import *

urlpatterns = [
    path("", PerfilUsuarioView.as_view(), name="Perfil"),
    path("login/", loginView, name="Login"),
    path("register/", registerView, name="Register"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="Logout"),
    path("editar/", editar_perfil, name="Editar"),
    path("crear-direccion/", crear_direccion, name="CrearDireccion"),
    path("editar-direccion/<int:direccion_id>/", editar_direccion, name="EditarDireccion"),
    path("pedidos/", pedidos_usuario, name="PedidosUsuario"),
    path("cambiar-pw/", cambiar_password, name="CambiarPW"),
    path('contactanos/', contactanos, name='Contactanos'),
    path('contactanos/gracias/', contactanosGracias, name='Contactanos2'),
    path('contactanos/mensajes/', mensajesContactanos, name='MensajesContactanos'),

]

