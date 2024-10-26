from django.shortcuts import render, reverse
from .models import Product, Category  # Make sure Category is imported
from django.http import HttpResponseRedirect

def show_main(request):
    category_name = request.GET.get('category')  # Get category from query parameters
    categories = Category.objects.all()
    
    # Filter products by category if category_name is specified
    if category_name:
        products = Product.objects.filter(category__name=category_name)
    else:
        products = Product.objects.all()

    return render(request, 'main.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_name,  # Pass selected category to the template
    })
