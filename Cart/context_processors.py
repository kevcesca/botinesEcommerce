from .cart import Cart  # Asegúrate de importar el módulo Cart correctamente

def cart_total(request):
    cart = Cart(request)
    items = cart.get_items()
    cantidad_total_productos = sum(item['cantidad'] for item in items)
    return {'cantidad_total_productos': cantidad_total_productos}
