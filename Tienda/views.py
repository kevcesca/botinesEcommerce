from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.db import connection
from decimal import Decimal
from .forms import ProductoForm
from .models import *
from Cart.cart import Cart


def login_redirect(request):
    messages.info(request, 'Por favor inicia sesión para continuar.')
    return redirect('Login')

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


class ProductoListView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

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


class ProductoCreateView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

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


class ProductoUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    
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


class ProductoDeleteView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('ListaProductos')


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    context = {'producto': producto}
    return render(request, 'detalleProducto.html', context)


def about(request):
    return render(request, 'about.html')