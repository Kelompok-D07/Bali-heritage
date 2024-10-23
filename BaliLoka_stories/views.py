from django.shortcuts import render, redirect
from BaliLoka_stories.forms import StoriesEntryForm
from BaliLoka_stories.models import StoriesEntry
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_stories(request):
    stories_entries = StoriesEntry.objects.all()
    print(request.user)
    context = {
        'stories_entries': stories_entries,
        'user': request.user
    }

    return render(request, "stories_page.html", context)

def create_stories_entry(request):
    form = StoriesEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_stories_entry.html", context)

@csrf_exempt
@require_POST
def add_stories_entry_ajax(request):
    name = request.POST.get("name")
    image = request.FILES.get("image")
    description = request.POST.get("description")
    user = request.user

    new_product = StoriesEntryForm(
        name=name,
        image=image,
        description=description,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def show_xml(request):
    data = StoriesEntry.objects.all()
    
def show_xml(request):
    data = StoriesEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = StoriesEntry.objects.all()
    
def show_json(request):
    data = StoriesEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")