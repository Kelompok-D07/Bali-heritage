from django.shortcuts import render, reverse, get_object_or_404
from .models import Product, Category, Restaurant
from Review.models import Review
from bookmarks.models import Bookmark  # Make sure Category is imported
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string


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