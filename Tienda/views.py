from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.db.models import Q
from .forms import ProductoForm
from .models import *
from Cart.cart import Cart

# Create your views here.
class ProductoList(ListView):
    model = Producto
    template_name = "productos.html"
    context_object_name = "productos"

    def get_queryset(self):
        queryset = Producto.objects.all()
        query = self.request.GET.get('q')
        categoria = self.request.GET.get('categoria')
        talla = self.request.GET.get('talla')
        tipo_cliente = self.request.GET.get('tipo_cliente')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query)
            )

        if categoria:
            queryset = queryset.filter(categoria__nombre=categoria)

        if talla:
            queryset = queryset.filter(talla__numeroDeTalla=talla)

        if tipo_cliente:
            queryset = queryset.filter(tipoDeCliente__nombre=tipo_cliente)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['tallas'] = Talla.objects.all()
        context['tipos_cliente'] = TipoDeCliente.objects.all()
        return context


def agregar_carrito(req):
    if req.method == "POST":
        product_id = req.POST.get('product_id')
        product = Producto.objects.get(id=product_id)
        cart = Cart(req)
        cart.add(product)
        
        # Agrega un mensaje de éxito
        messages.success(req, f"{product.nombre} agregado al carrito")

    # Redirige a la página ProductoList con el mensaje
    return redirect('Productos')


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


def ver_carrito(request):
    cart = Cart(request)
    items = cart.get_items()
    total = cart.get_total()
    return render(request, 'carrito.html', {'items': items, 'total': total})


def realizar_pedido(request):
    cart = Cart(request)
    
    # Aquí puedes procesar el pedido y la pasarela de pago
    # Por ejemplo, si estás usando Stripe, puedes crear una sesión de pago aquí
    
    # Una vez que se ha realizado el pedido y el pago, puedes vaciar el carrito
    cart.clear()
    
    # Redirige a una página de confirmación o de éxito del pedido
    return redirect('pagina_de_confirmacion')


def eliminar_del_carrito(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Producto.objects.get(id=product_id)
        cart = Cart(request)
        cart.remove(product)
    
    return redirect('Carrito')


def sumar_al_carrito(request, product_id):
    product = Producto.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product)
    return redirect('Carrito')


def restar_del_carrito(request, product_id):
    product = Producto.objects.get(id=product_id)
    cart = Cart(request)
    cart.decrement(product)
    return redirect('Carrito')


class ProductoListView(View):
    template_name = 'producto_list.html'

    def get(self, request):
        query = request.GET.get('q')
        if query:
            productos = Producto.objects.filter(
                Q(nombre__icontains=query) | Q(descripcion__icontains=query)
            )
        else:
            productos = Producto.objects.all()
        return render(request, self.template_name, {'productos': productos})



class ProductoCreateView(View):

    def get(self, request):
        form = ProductoForm()
        return render(request, 'producto_form.html', {'form': form})

    def post(self, request):
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('ListaProductos')
        return render(request, 'producto_form.html', {'form': form})


class ProductoUpdateView(View):
    
    def get(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        form = ProductoForm(instance=producto)
        return render(request, 'producto_form.html', {'form': form, 'producto': producto})

    def post(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('ListaProductos')
        return render(request, 'producto_form.html', {'form': form, 'producto': producto})


class ProductoDeleteView(View):
    def post(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('ListaProductos')


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    context = {'producto': producto}
    return render(request, 'detalleProducto.html', context)


def about(req):
    return render(req, 'about.html')