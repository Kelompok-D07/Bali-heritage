from django.shortcuts import render, redirect, reverse
from BaliLoka_stories.forms import StoriesEntryForm
from BaliLoka_stories.models import StoriesEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
import json
from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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
    print("pertama")
    name = request.POST.get("name")
    image = request.FILES.get("image")
    description = request.POST.get("description")

    new_product = StoriesEntry(
        name=name,
        image=image,
        description=description,
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

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

# @csrf_exempt
# def create_stories_flutter(request):
#     if request.method == 'POST':

#         data = json.loads(request.body)
#         new_stories = StoriesEntry.objects.create(
#             user=request.user,
#             name=data["name"],
#             image=data["image"],
#             description=data["description"]
#         )

#         new_stories.save()

#         return JsonResponse({"status": "success"}, status=200)
#     else:
#         return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def create_stories_flutter(request):
    if request.method == 'POST':
        # Parsing data JSON
        data = json.loads(request.body)

        # Pastikan ada data 'image' yang berupa string base64
        image_data = data.get("image", None)
        if image_data is None:
            return JsonResponse({"status": "error", "message": "Image is required"}, status=400)

        # Decode base64 menjadi file
        try:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]  # Ekstensi file, contoh: png, jpg
            image_file = ContentFile(base64.b64decode(imgstr), name=f"image.{ext}")
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Invalid image format"}, status=400)

        # Membuat entri baru
        new_stories = StoriesEntry.objects.create(
            user=request.user,
            name=data["name"],
            image=image_file,  # Simpan file
            description=data["description"]
        )

        new_stories.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

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