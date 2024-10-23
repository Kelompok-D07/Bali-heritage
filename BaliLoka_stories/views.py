from django.shortcuts import render, redirect
from BaliLoka_stories.forms import StoriesEntryForm
from BaliLoka_stories.models import StoriesEntry
from django.http import HttpResponse
from django.core import serializers

def show_stories(request):
    stories_entries = StoriesEntry.objects.all()
    context = {
        'stories': stories_entries
    }

    return render(request, "stories_page.html", context)

def create_stories_entry(request):
    form = StoriesEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_stories_entry.html", context)

def show_xml(request):
    data = StoriesEntry.objects.all()
    
def show_xml(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = MoodEntry.objects.all()