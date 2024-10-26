from django.contrib import admin

from django.contrib import admin
from .models import Product, Category, Restaurant

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Restaurant)
