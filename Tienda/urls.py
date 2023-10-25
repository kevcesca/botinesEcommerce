from django.contrib import admin
from django.urls import path
from Tienda.views import *

urlpatterns = [
    path("", ProductoList.as_view(), name="Productos"),
    path("about", about, name="About"),
    path('detalles/<int:producto_id>/', detalle_producto, name='DetalleProducto'),
    path('productos/', ProductoListView.as_view(), name='ListaProductos'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
    path('login-redirect/', login_redirect, name='login_redirect'),
]

