from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.db import connection, transaction
from decimal import Decimal
from Tienda.models import *
from Cart.cart import Cart


# Create your views here.
@login_required
def agregar_carrito(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('cantidad', 1))
        product = Producto.objects.get(id=product_id)
        cart = Cart(request)
        
        for _ in range(quantity):
            added = cart.add(product)
            if not added:
                messages.error(request, f"No se puede agregar más de {product.cantidad} de {product.nombre}")
                return redirect('Productos')
        
        # Agrega un mensaje de éxito
        messages.success(request, f"{product.nombre} agregado al carrito")

    # Redirige a la página ProductoList con el mensaje
    return redirect('Productos')


@login_required
def actualizar_cantidad(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        cantidad = int(request.POST.get('cantidad'))
        product = Producto.objects.get(id=product_id)
        cart = Cart(request)
        
        if cantidad > 0:
            cart.update_quantity(product, cantidad)
        else:
            cart.remove(product)
    
    return redirect('Carrito')


@login_required
def ver_carrito(request):
    cart = Cart(request)
    items = cart.get_items()
    total = cart.get_total()
    cantidad_total_productos = sum(item['cantidad'] for item in items)
    return render(request, 'carrito.html', {'items': items, 'total': total, 'cantidad_total_productos': cantidad_total_productos})


@login_required
def pagina_de_confirmacion(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if request.user == pedido.cliente:
        return render(request, 'confirmacionPedido.html', {'pedido': pedido})
    else:
        messages.error(request, "No tienes permiso para ver este pedido.")
        return redirect('Inicio')

def es_propietario_pedido(user, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    return user == pedido.cliente

@login_required
def pagina_de_confirmacion_restringida(request, pedido_id):
    es_propietario = lambda u: es_propietario_pedido(u, pedido_id)
    return user_passes_test(es_propietario, login_url='Inicio')(pagina_de_confirmacion)(request, pedido_id)


@login_required
def realizar_pedido(request, direccion_id):
    cart = Cart(request)
    direccion_seleccionada = Direccion.objects.get(id=direccion_id)
    totalCarrito = cart.get_total()

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(id) from tienda_pedido")
            result = cursor.fetchone()
            last_id = result[0]

        new_id = last_id + 1 if last_id else 1

        pedido = Pedido(
            id=new_id,
            cliente=request.user,
            monto_total=totalCarrito,
            direccion=direccion_seleccionada,
            status='En Camino'
        )

        pedido.generar_referencia_unica()  # Generar referencia antes de guardar
        pedido.save()  # Guardar el pedido para obtener un ID válido

        for item in cart.get_items():
            product_id = item['product_id']
            producto = Producto.objects.get(id=product_id)
            cantidad_actual = producto.cantidad - item['cantidad']
            if cantidad_actual <= 0: # Comprobar el stock
                producto.disponible = False
                producto.cantidad = 0
            else:
                producto.cantidad = cantidad_actual
            producto.save()

            pedido.productos.add(producto)  # Agregar los productos

        # Vaciar el carrito una vez que se haya realizado el pedido
        cart.clear()

    # Redirigir a la página de confirmación de pedidos con el ID del pedido
    return redirect('PedidoRealizado', pedido_id=pedido.id)


@login_required
def confirmar_pedido(request):
    direcciones = Direccion.objects.filter(usuario=request.user)
    total = Cart(request).get_total()
    return render(request, 'confirmarPedido.html', {'direcciones': direcciones, 'total': total})


@login_required
def eliminar_del_carrito(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Producto.objects.get(id=product_id)
        cart = Cart(request)
        cart.remove(product)
    
    return redirect('Carrito')


@login_required
def sumar_al_carrito(request, product_id):
    product = Producto.objects.get(id=product_id)
    cart = Cart(request)
    added = cart.add(product)
    if not added:
        messages.error(request, f"No se puede agregar más de {product.cantidad} de {product.nombre}")
    return redirect('Carrito')


@login_required
def restar_del_carrito(request, product_id):
    product = Producto.objects.get(id=product_id)
    cart = Cart(request)
    cart.decrement(product)
    return redirect('Carrito')
