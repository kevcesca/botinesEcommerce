from decimal import Decimal
from django.conf import settings
from Tienda.models import Producto

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart
        
    def add(self, product):
        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                "product_id": product.id,
                "nombre": product.nombre,
                "cantidad": 1,
                "precio": str(product.precio),
                "imagen": product.imagen1.url
            }
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    value["cantidad"] = value["cantidad"] + 1
                    break
        self.save()
    
    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value["cantidad"] = value["cantidad"] - 1
                if value["cantidad"] < 1:
                    self.remove(product)
                else:
                    self.save()
                
                break
            else:
                print("El producto no existe en el carrito")
    
    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True 
    
    def get_total(self):
        total = Decimal(0)
        for item_id, item in self.cart.items():
            product = Producto.objects.get(id=item['product_id'])
            total += Decimal(item['precio']) * item['cantidad']
        return total

    def get_items(self):
        cart_items = []
        for item_id, item in self.cart.items():
            product = Producto.objects.get(id=item['product_id'])
            subtotal = Decimal(item['precio']) * item['cantidad']
            cart_items.append({
                'product_id': item['product_id'],
                'nombre': item['nombre'],
                'precio': item['precio'],
                'cantidad': item['cantidad'],
                'subtotal': subtotal,
                'imagen': item['imagen'],
            })
        return cart_items
    
    def update_quantity(self, product, quantity):
        product_id = str(product.id)
        
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['cantidad'] = quantity
            else:
                self.remove(product)
            self.save()