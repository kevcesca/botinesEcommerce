# Generated by Django 4.2.5 on 2023-10-17 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Tienda", "0003_pedido_delete_compra"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto",
            name="precioDescuento",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Precio con descuento"
            ),
        ),
    ]
