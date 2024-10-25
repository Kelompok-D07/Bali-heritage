from django.shortcuts import render, redirect
from BaliLoka_stories.forms import StoriesEntryForm
from BaliLoka_stories.models import StoriesEntry
from django.http import HttpResponse
from django.core import serializers

def show_bookmarks(request):
    context = {
        'name': 'User',
        'description': 'Hello'
    }
    return render(request, "bookmarks.html", context)