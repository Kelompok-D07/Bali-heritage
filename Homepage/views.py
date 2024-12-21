import json
from django.shortcuts import render, reverse, get_object_or_404
from .models import Product, Category, Restaurant
from Review.models import Review
from bookmarks.models import Bookmark  # Make sure Category is imported
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
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

def get_products(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

    
@csrf_exempt
def create_product_flutter(request):
    print('hello')
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

            # Retrieve the Category and Restaurant based on their names
            try:
                category = get_object_or_404(Category, name=product_category_name)
                print(category)
            except Http404:
                return JsonResponse({"status": "error", "message": "Category not found"}, status=404)

            try:
                restaurant = get_object_or_404(Restaurant, name=restaurant_name)
                print(restaurant.description)
            except Http404:
                return JsonResponse({"status": "error", "message": "Restaurant not found"}, status=404)

            # Create the new product
            print('hello2')
            print(product_image)
            new_product = Product.objects.create(
                name=product_name,
                description=product_description,
                price=float(product_price),
                image=product_image,
                category=category,
                restaurant_name=restaurant
            )
            print('hello3')
            new_product.save()

            return JsonResponse({"status": "success", "message": "Product has been added successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=405)

@csrf_exempt
def filter_product_flutter(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            category_name = data.get('category')

            if category_name:  # If a category is provided, filter products by that category
                try:
                    category = get_object_or_404(Category, name=category_name)
                except Http404:
                    return JsonResponse({"status": "error", "message": "Category not found"}, status=404)

                products = Product.objects.filter(category=category)
            else:  # If no category is provided, return all products
                products = Product.objects.all()

            serialized_products = serializers.serialize("json", products)

            return JsonResponse({"status": "success", "data": json.loads(serialized_products)}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=405)
    
@csrf_exempt
def get_restaurant_flutter(request):
    print('hello')
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            restaurant_name = data.get('restaurant_name')

            if restaurant_name:  # If a restaurant name is provided
                try:
                    print('hello2')
                    print(data)
                    print(restaurant_name)
                    
                    # Assuming restaurant_name is an ID or a unique identifier
                    restaurant = get_object_or_404(Restaurant, id=restaurant_name)
                    print(restaurant.name)
                    
                    # Get products related to the restaurant
                    products = Product.objects.filter(restaurant_name=restaurant)
                    print(products)

                    # Serialize restaurant and products into JSON
                    restaurant_data = serializers.serialize("json", [restaurant])
                    products_data = serializers.serialize("json", products)

                    # Combine restaurant and product data into the response
                    response_data = {
                        "restaurant": json.loads(restaurant_data)[0],  # Convert to dictionary
                        "products": json.loads(products_data)  # Convert to list of dictionaries
                    }

                    print(response_data)

                    return JsonResponse({"status": "success", "data": response_data}, status=200)

                except Http404:
                    return JsonResponse({"status": "error", "message": "Restaurant not found"}, status=404)

            else:
                return JsonResponse({"status": "error", "message": "Restaurant name is required."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=405)