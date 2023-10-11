from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UsuarioPersonalizado(AbstractUser):
    imagen = models.ImageField(upload_to='avatares', blank=True, null=True, default='avatares/avatar.png')
    activo = models.BooleanField(default=True)

class Direccion(models.Model):
    calle = models.CharField(max_length=255, verbose_name="Calle")
    numero = models.PositiveIntegerField(verbose_name="Número")
    barrio = models.CharField(max_length=100, verbose_name="Barrio")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    provincia = models.CharField(max_length=100, verbose_name="Provincia")
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal")
    comentarios = models.TextField(max_length=300, verbose_name="Comentarios")
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='direcciones')

    def __str__(self):
        return f'{self.numero} {self.calle}, {self.barrio}, {self.ciudad}, {self.provincia}, {self.codigo_postal}'


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    correo = models.EmailField(max_length=100, verbose_name="Correo Electrónico")
    mensaje = models.TextField(verbose_name="Mensaje")
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    leido = models.BooleanField(default=False, verbose_name="Leído")  # Nuevo campo

    def __str__(self):
        return self.nombre

