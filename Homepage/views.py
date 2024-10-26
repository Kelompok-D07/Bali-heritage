from django.shortcuts import render, reverse, get_object_or_404
from .models import Product, Category, Restaurant  # Make sure Category is imported
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

def restaurant(request):
    # Retrieve the restaurant ID from query parameters
    restaurant_name = request.GET.get('restaurant_name')
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)
    products = Product.objects.filter(restaurant_name=restaurant)
    review = restaurant.review.all()
    # Render the template with restaurant details, products, and categories
    return render(request, 'restaurant.html', {
        'restaurant': restaurant,
        'products': products,
        'reviews': review,
    })