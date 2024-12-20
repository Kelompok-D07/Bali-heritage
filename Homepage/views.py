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
    print(request.headers)
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract product details from the received data
            product_name = data.get('name')
            product_description = data.get('description')
            product_price = data.get('price')
            product_image = data.get('image')
            product_category_name = data.get('category')
            restaurant_name = data.get('restaurant_name')

            # Validate required fields
            if not all([product_name, product_description, product_price, product_image, product_category_name, restaurant_name]):
                return JsonResponse({"status": "error", "message": "All fields are required!"}, status=400)

            # Retrieve the Category and Restaurant based on their names
            category = get_object_or_404(Category, name=product_category_name)
            restaurant = get_object_or_404(Restaurant, name=restaurant_name)

            # Create the new product
            new_product = Product.objects.create(
                name=product_name,
                description=product_description,
                price=product_price,
                image=product_image,
                category=category,
                restaurant=restaurant
            )
        
            return JsonResponse({"status": "success", "message": "Product has been added successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=405)