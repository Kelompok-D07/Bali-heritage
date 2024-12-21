import json
from django.shortcuts import render, redirect, get_object_or_404
from bookmarks.models import Bookmark
from Homepage.models import Category, Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import EditNotesForm
from django.template.loader import render_to_string




@login_required(login_url='/')
def show_bookmarks(request):
    selected_category = request.GET.get("category", None)
    bookmarks = Bookmark.objects.filter(user=request.user)
    categories = Category.objects.all()
    context = {
        'bookmarks': bookmarks,
        'categories': categories,
        'selected_category': selected_category,
        'alert': None
    }
    return render(request, "bookmarks.html", context)

def add_to_bookmarks(request):
    if request.method == 'POST':
        user_username = request.POST.get('user_username')
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)

        if Bookmark.objects.filter(user=request.user, product=product).exists():
            item = Bookmark.objects.get(user=request.user, product=product)
            item_name = item.product.name
            item.delete()
            return JsonResponse({'status': 'deleted', 'message': f"Makanan {item_name} sudah terdelete dari dalam bookmarks Anda."})
        else:
            Bookmark.objects.create(user=request.user, product=product)
            return JsonResponse({'status': 'added', 'message': 'Product added to bookmarks successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})



@csrf_exempt
def delete_bookmarks_item(request, item_id):
    print("deleted item: " + str(item_id))
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                item = Bookmark.objects.get(pk=item_id, user=request.user)
                item_name = item.product.name
                item.delete()
                return JsonResponse({'status': item_name + " removed from Bookmarks"})
            except Bookmark.DoesNotExist:
                return JsonResponse({'status': item_name + " not found in Bookmarks"}, status=404)
        else:
            return JsonResponse({'status': "Login to continue"}, status=403)
    return JsonResponse({'status': "Invalid request method"}, status=400)


@login_required(login_url='/')
def filter_bookmarks(request):
    if request.method == 'GET':
        category_name = request.GET.get('category')
        
        if category_name:
            bookmarks = Bookmark.objects.filter(user=request.user, product__category__name=category_name)
        else:
            bookmarks = Bookmark.objects.filter(user=request.user)
        
        html = render_to_string('card_product.html', {'bookmarks': bookmarks}, request=request)
        return JsonResponse({'status': 'success', 'html': html})  # Mengembalikan HTML yang difilter
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def edit_notes(request, item_id):
    if request.method == 'POST':
        bookmark = get_object_or_404(Bookmark, id=item_id, user=request.user)
        form = EditNotesForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'notes': bookmark.notes})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    

## Flutter
# @login_required(login_url='/')
def show_json(request):
    data = Bookmark.objects.filter(user=request.user)

    bookmarks_data = [
        {
            "model": "bookmarks.bookmark",
            "pk": bookmark.pk,
            "fields": {
                "user": bookmark.user.username,
                "user_id": bookmark.user.id,
                "product": bookmark.product.name,
                "product_id": bookmark.product.id,
                "image": bookmark.product.image,
                "notes": bookmark.notes,
                "description": bookmark.product.description
            }
        }
        for bookmark in data
    ]

    return JsonResponse(bookmarks_data, safe=False)


@csrf_exempt
def edit_notes_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_name = data.get('item_name')  # Ambil ID bookmark
            new_notes = data.get('new_notes')  # Ambil notes baru
            bookmark = get_object_or_404(Bookmark, product__name=product_name, user=request.user)

            # Update notes dan simpan ke database
            bookmark.notes = new_notes
            bookmark.save()
            return JsonResponse({'status': 'success', 'message': 'Notes updated successfully', 'new_notes': bookmark.notes})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def delete_bookmarks_flutter(request, product_name):
    if request.method == 'POST':
        try:
            item = get_object_or_404(Bookmark, product__name=product_name, user=request.user)
            item_name = item.product.name
            item.delete()
            return JsonResponse({'status': 'success'})
        except Bookmark.DoesNotExist:
            return JsonResponse({'status': item_name + " not found in Bookmarks"}, status=404)
    return JsonResponse({'status': "Invalid request method"}, status=400)

