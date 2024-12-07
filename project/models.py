from django.db import models
from django.db.models import Sum, F
from django.contrib.auth.models import User

class Business(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def total_revenue(self):
        """Calculate total revenue based on transactions"""
        revenue = Transaction.objects.filter(product__business=self).aggregate(
            total_revenue=Sum(F('amount') * F('product__price'))
        )['total_revenue']
        return round(revenue or 0, 2)

class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    picture_url = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    @property
    def amount_sold(self):
        """Calculate the total amount sold for this product."""
        total_sold = Transaction.objects.filter(product=self).aggregate(
            total_sold=Sum('amount')
        )['total_sold']
        return total_sold or 0

class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer.username} bought {self.product.name}'

    @property
    def total_spent(self):
        """Calculate the total amount spent on this transaction."""
        return self.amount * self.product.price
