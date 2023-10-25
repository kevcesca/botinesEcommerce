from django.contrib import admin
from django.urls import path
from Cart.views import *

urlpatterns = [
    path('', ver_carrito, name='Carrito'),
    path("agregar-carrito", agregar_carrito, name="AgregarCarrito"),
    path('sumar/<int:product_id>', sumar_al_carrito, name='SumarCarrito'),
    path('restar/<int:product_id>', restar_del_carrito, name='RestarCarrito'),
    path('eliminar/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-cantidad/', actualizar_cantidad, name='actualizar_cantidad'),
    path('confirmar-pedido/', confirmar_pedido, name='ConfirmarPedido'),
    path('realizar-pedido/<int:direccion_id>/', realizar_pedido, name='RealizarPedido'),
    path('pedido-realizado/<int:pedido_id>', pagina_de_confirmacion, name='PedidoRealizado'),
]

