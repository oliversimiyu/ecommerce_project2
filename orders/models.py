from django.db import models
from products.models import Product
from django.conf import settings
from typing import Any
from decimal import Decimal

# Create your models here.

class Order(models.Model):
    user: settings.AUTH_USER_MODEL = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                     on_delete=models.CASCADE,
                                                     related_name='orders')
    first_name: str = models.CharField(max_length=50)
    last_name: str = models.CharField(max_length=50)
    email: str = models.EmailField()
    address: str = models.CharField(max_length=250)
    postal_code: str = models.CharField(max_length=20)
    city: str = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid: bool = models.BooleanField(default=False)
    discount: Decimal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self) -> str:
        return f'Order {self.id}'

    def get_total_cost(self) -> Decimal:
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order: 'Order' = models.ForeignKey('Order',
                                   related_name='items',
                                   on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product,
                                       related_name='order_items',
                                       on_delete=models.CASCADE)
    price: Decimal = models.DecimalField(max_digits=10,
                                       decimal_places=2)
    quantity: int = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)

    def get_cost(self) -> Decimal:
        return self.price * self.quantity
