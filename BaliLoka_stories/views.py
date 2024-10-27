from django.shortcuts import render, redirect, reverse
from BaliLoka_stories.forms import StoriesEntryForm
from BaliLoka_stories.models import StoriesEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse

def show_stories(request):
    stories_entries = StoriesEntry.objects.all()
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

    if request.method == request.POST:
        new_product = StoriesEntryForm(
            name=name,
            image=image,
            description=description,
            user=user
        )
        new_product.save()

    return HttpResponse(b"CREATED", status=201)

# @csrf_exempt
# @require_POST
# def add_stories_entry_ajax(request):
#     form = StoriesEntryForm(request.POST, request.FILES)
    
#     if form.is_valid():
#         new_story = form.save(commit=False)  # Jangan langsung simpan ke database
#         new_story.user = request.user        # Tambahkan user ke objek yang akan disimpan
#         new_story.save()                     # Simpan objek ke database
#         return HttpResponse(b"CREATED", status=201)
#     else:
#         return HttpResponse(b"INVALID", status=400)

def edit_stories(request, id):
    # Get mood entry berdasarkan id
    stories_entries = StoriesEntry.objects.get(pk = id)

    # Set mood entry sebagai instance dari form
    form = StoriesEntryForm(request.POST or None, instance=stories_entries)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('BaliLoka_stories:show_stories'))

    context = {'form': form}
    return render(request, "edit_stories.html", context)

def delete_stories(request, id):
    # Get mood berdasarkan id
    stories_entries = StoriesEntry.objects.get(pk = id)
    # Hapus mood
    stories_entries.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('BaliLoka_stories:show_stories'))

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