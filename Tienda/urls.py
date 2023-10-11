from django.contrib import admin
from django.urls import path
from Tienda.views import *

urlpatterns = [
    path("", ProductoList.as_view(), name="Productos"),
    path("about", about, name="About"),
    path('detalles/<int:producto_id>/', detalle_producto, name='DetalleProducto'),
    path("agregar-carrito", agregar_carrito, name="AgregarCarrito"),
    path('carrito/', ver_carrito, name='Carrito'),
    path('carrito/sumar/<int:product_id>', sumar_al_carrito, name='SumarCarrito'),
    path('carrito/restar/<int:product_id>', restar_del_carrito, name='RestarCarrito'),
    path('carrito/eliminar/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/actualizar-cantidad/', actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/realizar-pedido/', realizar_pedido, name='realizar_pedido'),
    path('productos/', ProductoListView.as_view(), name='ListaProductos'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),

]

