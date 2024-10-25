from django.shortcuts import render, redirect
from bookmarks.models import Bookmark
from django.http import HttpResponse
from django.core import serializers
# from django.contrib.auth.decorators import login_required

# @login_required()
def show_bookmarks(request):
    # bookmarks = Bookmark.objects.filter(user=request.user)
    context = {'bookmarks': "name"}
    return render(request, "bookmarks.html", context)