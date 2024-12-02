from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Business, Product, Transaction

# Register your models
admin.site.register(User)
admin.site.register(Business)
admin.site.register(Product)
admin.site.register(Transaction)
