from django.shortcuts import render, redirect, get_object_or_404
from bookmarks.models import Bookmark
from Homepage.models import Category
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/')
def show_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    categories = Category.objects.all()
    context = {'bookmarks': bookmarks,
               'categories': categories}
    return render(request, "bookmarks.html", context)


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


