import json
from django.shortcuts import render, reverse, get_object_or_404
from .models import Product, Category, Restaurant
from Review.models import Review
from bookmarks.models import Bookmark  # Make sure Category is imported
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


def show_main(request):
    category_name = request.GET.get('category')  # Get category from query parameters
    categories = Category.objects.all()
    
    # Filter products by category if category_name is specified
    if category_name:
        products = Product.objects.filter(category__name=category_name)
    else:
        products = Product.objects.all()
    bookmarked_product_ids = Bookmark.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []

    return render(request, 'main.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_name or None,  # Pass selected category to the template
        'bookmarked_product_ids': list(bookmarked_product_ids)
    })

def restaurant(request):
    restaurant_name = request.GET.get('restaurant_name')
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)
    products = Product.objects.filter(restaurant_name=restaurant)
    reviews = restaurant.review.all() 
    # Render the template with restaurant details, products, and categories
    return render(request, 'restaurant.html', {
        'restaurant': restaurant,
        'products': products,
        'reviews': reviews,
    })

# Filter dengan Ajax
def filter_product(request):
    if request.method == 'GET':
        category_name = request.GET.get('category')  # Mengambil nama kategori
        
        # Filter Product berdasarkan kategori yang dipilih
        if category_name:
            products = Product.objects.filter(category__name=category_name)
        else:
            products = Product.objects.all()  # Jika kategori kosong, tampilkan semua

        bookmarked_product_ids = Bookmark.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []
        
        # Render ulang template dengan product yang difilter
        html = render_to_string('card_product_main.html', {'products': products, 'bookmarked_product_ids': list(bookmarked_product_ids)}, request=request)
        return JsonResponse({'status': 'success', 'html': html})  # Mengembalikan HTML yang difilter
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_categories(request):
    data = Category.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_restaurants(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

    
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body)

            # Create new Product instance
            new_product = Product.objects.create(
                name=data["name"],
                description=data.get("description", ""),  # Use default empty string if not provided
                price=data["price"],
                image=data["image"],
                category_id=data["category"],  # Assume category ID is passed
                restaurant_name_id=data["restaurant_name"]  # Assume restaurant ID is passed
            )

            # Save the Product instance
            new_product.save()

            # Return success response
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    # Return error for non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=401)
