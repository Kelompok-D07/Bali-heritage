from django.shortcuts import render, redirect, get_object_or_404
from bookmarks.models import Bookmark
from Homepage.models import Category, Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import EditNotesForm



@login_required(login_url='/')
def show_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    categories = Category.objects.all()
    context = {
        'bookmarks': bookmarks,
        'categories': categories,
        'alert': None  # Default alert is None
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


@csrf_exempt
def edit_notes(request, item_id):
    if request.method == 'POST':
        bookmark = get_object_or_404(Bookmark, id=item_id, user=request.user)
        form = EditNotesForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'notes': bookmark.notes})
        return JsonResponse({'status': 'error', 'errors': form.errors})