from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    product_name = models.CharField(max_length=100)
    order_date = models.DateField()

    def __str__(self):
        return f"{self.product_name} ({self.customer.name})"
