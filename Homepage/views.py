from django.shortcuts import render
from .models import Product, Category  # Make sure Category is imported

def show_main(request):
    products = Product.objects.all()  # Display all products by default
    categories = Category.objects.all()  # Fetch all categories to display in the template
    return render(request, 'main.html', {'products': products, 'categories': categories})