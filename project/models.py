from django.db import models

# Business Model
class Business(models.Model):
    name = models.CharField(max_length=100)
    date_of_establishment = models.DateField()

    def __str__(self):
        return self.name


# User Model
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='users'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    picture = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products'
    )
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='products'
    )

    def __str__(self):
        return self.name


# Transaction Model
class Transaction(models.Model):
    date_of_transaction = models.DateField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='transactions'
    )
    sold_by = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='sales'
    )
    bought_by = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='purchases'
    )

    def __str__(self):
        return f"Transaction on {self.date_of_transaction}"
