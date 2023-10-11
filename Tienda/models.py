from django.db import models
from Perfil.models import UsuarioPersonalizado, Direccion
from django.utils import timezone
import uuid

# Create your models here.
class TipoDeCliente(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de cliente")
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Categoria")
    
    def __str__(self):
        return self.nombre

class Talla(models.Model):
    tipoDeCliente = models.ForeignKey(TipoDeCliente, on_delete=models.CASCADE, verbose_name="Tipo de cliente")
    numeroDeTalla = models.CharField(max_length=10, verbose_name="Numero de talla")
    
    def __str__(self):
        return f"({self.tipoDeCliente}) {self.numeroDeTalla}"

class Producto(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    imagen1 = models.ImageField(upload_to='productos', blank=True, null=True, default='productos/default.png', verbose_name="Imagen 1 del producto")
    imagen2 = models.ImageField(upload_to='productos', blank=True, null=True, default='productos/default.png', verbose_name="Imagen 2 del producto")
    imagen3 = models.ImageField(upload_to='productos', blank=True, null=True, default='productos/default.png', verbose_name="Imagen 3 del producto")
    precio = models.PositiveIntegerField(verbose_name="Precio")
    precioDescuento = models.PositiveIntegerField(verbose_name="Precio con descuento")
    descripcion = models.TextField(max_length=500, verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    talla = models.ManyToManyField(Talla, related_name='productosTalla', blank=True, verbose_name="Talla")
    categoria = models.ManyToManyField(Categoria, related_name='productosCategoria', blank=True, verbose_name="Categoria")
    tipoDeCliente = models.ManyToManyField(TipoDeCliente, related_name='productosClientes', blank=True, verbose_name="Tipo de cliente")
    
    def __str__(self):
        return f"({self.nombre})"

class Compra(models.Model):
    STATUS_CHOICES = (
        ('Entregado', 'Entregado'),
        ('En Camino', 'En Camino'),
        ('Cancelado', 'Cancelado'),
    )
    
    cliente = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, verbose_name="Cliente")
    productos = models.ManyToManyField('Producto', related_name='compras', verbose_name="Productos")
    monto_total = models.PositiveIntegerField(verbose_name="Monto Total")
    fecha = models.DateField(default=timezone.now, verbose_name="Fecha")
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, verbose_name="Dirección")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Estado")
    referencia = models.CharField(max_length=50, unique=True, verbose_name="Referencia")
    
    # Metodos
    def save(self, *args, **kwargs):
        # Calcula el monto total sumando los precios de los productos
        self.monto_total = sum(producto.precio for producto in self.productos.all())
        super(Compra, self).save(*args, **kwargs)
    
    def generar_referencia_unica(self):
        # Genera una referencia única utilizando uuid4
        unique_id = str(uuid.uuid4().hex[:10])  # Puedes ajustar la longitud de la referencia según tus necesidades
        self.referencia = unique_id
    
    def __str__(self):
        return f"Compra de {self.cliente.username} - Referencia: {self.referencia}"


class ItemCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
