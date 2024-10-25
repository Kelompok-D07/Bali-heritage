from django.shortcuts import render, redirect
from bookmarks.models import Bookmark
from Homepage.models import Category
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def show_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    categories = Category.objects.all()
    context = {'bookmarks': bookmarks,
               'categories': categories}
    return render(request, "bookmarks.html", context)