from django.contrib import admin
from .models import Business, Product, Transaction

# Register your models here.
admin.site.register(Business)
admin.site.register(Product)
admin.site.register(Transaction)