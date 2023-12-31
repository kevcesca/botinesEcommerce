# Generated by Django 4.2.5 on 2023-10-06 01:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Perfil", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255, verbose_name="Categoria")),
            ],
        ),
        migrations.CreateModel(
            name="TipoDeCliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(max_length=255, verbose_name="Tipo de cliente"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Talla",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "numeroDeTalla",
                    models.CharField(max_length=10, verbose_name="Numero de talla"),
                ),
                (
                    "tipoDeCliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Tienda.tipodecliente",
                        verbose_name="Tipo de cliente",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Producto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=50, verbose_name="Nombre")),
                (
                    "imagen1",
                    models.ImageField(
                        blank=True,
                        default="productos/default.png",
                        null=True,
                        upload_to="productos",
                        verbose_name="Imagen 1 del producto",
                    ),
                ),
                (
                    "imagen2",
                    models.ImageField(
                        blank=True,
                        default="productos/default.png",
                        null=True,
                        upload_to="productos",
                        verbose_name="Imagen 2 del producto",
                    ),
                ),
                (
                    "imagen3",
                    models.ImageField(
                        blank=True,
                        default="productos/default.png",
                        null=True,
                        upload_to="productos",
                        verbose_name="Imagen 3 del producto",
                    ),
                ),
                ("precio", models.PositiveIntegerField(verbose_name="Precio")),
                (
                    "precioDescuento",
                    models.PositiveIntegerField(verbose_name="Precio con descuento"),
                ),
                (
                    "descripcion",
                    models.CharField(max_length=500, verbose_name="Descripción"),
                ),
                ("cantidad", models.PositiveIntegerField(verbose_name="Cantidad")),
                (
                    "disponible",
                    models.BooleanField(default=True, verbose_name="Disponible"),
                ),
                (
                    "categoria",
                    models.ManyToManyField(
                        blank=True,
                        related_name="productosCategoria",
                        to="Tienda.categoria",
                        verbose_name="Categoria",
                    ),
                ),
                (
                    "talla",
                    models.ManyToManyField(
                        blank=True,
                        related_name="productosTalla",
                        to="Tienda.talla",
                        verbose_name="Talla",
                    ),
                ),
                (
                    "tipoDeCliente",
                    models.ManyToManyField(
                        blank=True,
                        related_name="productosClientes",
                        to="Tienda.tipodecliente",
                        verbose_name="Tipo de cliente",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemCarrito",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.PositiveIntegerField(verbose_name="Cantidad")),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Tienda.producto",
                        verbose_name="Producto",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Compra",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "monto_total",
                    models.PositiveIntegerField(verbose_name="Monto Total"),
                ),
                (
                    "fecha",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Fecha"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Entregado", "Entregado"),
                            ("En Camino", "En Camino"),
                            ("Cancelado", "Cancelado"),
                        ],
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                (
                    "referencia",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Referencia"
                    ),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Cliente",
                    ),
                ),
                (
                    "direccion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Perfil.direccion",
                        verbose_name="Dirección",
                    ),
                ),
                (
                    "productos",
                    models.ManyToManyField(
                        related_name="compras",
                        to="Tienda.producto",
                        verbose_name="Productos",
                    ),
                ),
            ],
        ),
    ]
