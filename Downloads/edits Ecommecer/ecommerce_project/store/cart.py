from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product.inventory <= 0:
            return
        existing = self.cart.get(product_id, 0)
        new_qty = existing + quantity
        if new_qty > product.inventory:
            new_qty = product.inventory
        self.cart[product_id] = new_qty
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        try:
            quantity = int(quantity)
        except Exception:
            quantity = self.cart.get(product_id, 0)
        if quantity <= 0:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()
            return
        if product.inventory <= 0:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()
            return
        if quantity > product.inventory:
            quantity = product.inventory
        self.cart[product_id] = quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            quantity = self.cart[str(product.id)]
            yield {
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total_price': product.price * quantity
            }

    def get_total_price(self):
        return sum(item['total_price'] for item in self)
    
    def clear(self):
        del self.session['cart']
        self.save()
