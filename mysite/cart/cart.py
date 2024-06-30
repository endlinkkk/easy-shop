from decimal import Decimal
from django.conf import settings
from django.http import HttpRequest
from catalog.models import Product
from catalog.serializers import ProductSerializer


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def get_products(self) -> ProductSerializer:
        product_ids = self.cart.keys()
        products = [product for product in Product.objects.filter(id__in=product_ids)]
        quantitys = [self.cart[p_id]["quantity"] for p_id in self.cart.keys()]
        serialized = ProductSerializer(products, many=True)
        for i, d in enumerate(serialized.data):
            d["count"] = quantitys[i]
            d["reviews"] = len(d["reviews"])
        return serialized

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product: Product, quantity: int = 1):
        product_id = str(product.id)
        self.cart[product_id]["quantity"] -= quantity
        if self.cart[product_id]["quantity"] <= 0:
            self.delete(product)
        self.save()

    def save(self):
        self.session.modified = True

    def delete(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
