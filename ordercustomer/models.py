from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    table_number = models.CharField(max_length=20)

    items = models.JSONField()

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )

    item = models.ForeignKey(
        "menu.FoodItem",
        on_delete=models.PROTECT
    )

    
