from django.contrib import admin
from .models import *

class TallaAdmin(admin.ModelAdmin):
    list_filter = ["tipoDeCliente", "numeroDeTalla"]

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion", "precio"]
    search_fields = ["nombre", "descripcion"]
    list_filter = ["talla", "categoria", "tipoDeCliente"]

# Register your models here.
admin.site.register(TipoDeCliente)
admin.site.register(Categoria)
admin.site.register(Talla, TallaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido)




