from django.db import models


class Customer(models.Model):
    name = models.CharField(
        max_length=150,
    )
    phone = models.CharField(
        max_length=10, 
    )

    table_number = models.CharField(
        max_length=10,
    )

    encrypted_phone = models.CharField(
        max_length=1000,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.phone}"