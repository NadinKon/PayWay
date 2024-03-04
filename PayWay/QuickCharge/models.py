from django.db import models
from decimal import Decimal

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)  # Например USD, EUR

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} from {self.created_at}"

    def total_cost(self):
        total = sum(item.price for item in self.items.all())
        discount = self.get_discount_amount()
        tax_rate = self.tax.percentage if hasattr(self, 'tax') else Decimal('0')
        tax_rate = Decimal(str(tax_rate)) / Decimal('100.0')
        return (total - discount) * (Decimal('1.0') + tax_rate)

    def get_discount_amount(self):
        if hasattr(self, 'discount'):
            return (self.discount.percentage / 100) * sum(item.price for item in self.items.all())
        return 0

class Discount(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='discount')
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Процент скидки

    def __str__(self):
        return f"{self.percentage}% for Order {self.order.id}"

class Tax(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tax')
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Процент налога

    def __str__(self):
        return f"{self.percentage}% for Order {self.order.id}"
