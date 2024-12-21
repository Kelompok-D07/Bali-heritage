import json
from django.shortcuts import render, redirect, reverse, get_object_or_404
from Review.models import Review
from Review.forms import ReviewForm
from Homepage.models import Restaurant
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers

@login_required(login_url='/')
def show_main(request):
    context = {}

    return render(request, "main.html", context)

def create_review_entry(request, restaurant_id):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('Homepage:main')

    # Get the restaurant using the UUID directly (no need for UUID conversion)
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Form handling
    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.restaurant = restaurant
        review.save()
        url = reverse('Homepage:restaurant') + f'?restaurant_name={restaurant.name}'

        # Redirect to the URL with query string
        return redirect(url)

    return render(request, "create_review_entry.html", {'form': form, 'restaurant': restaurant})

def review_store_detail(request, id):
    # Ambil review yang terkait dengan store tertentu
    restaurant = get_object_or_404(Restaurant, pk=id)
    reviews = restaurant.review.all()
    return render(request, 'restaurant.html', {
        'restaurant': restaurant,
        'reviews': reviews,
    })

def show_xml(request):
    data = Review.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Review.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_review(request, id):
    # Get review berdasarkan id
    review = get_object_or_404(Review, pk=id)
    restaurant = review.restaurant

    # Pastikan hanya user yang menulis review bisa mengeditnya
    if review.user != request.user:
        return redirect('Homepage:restaurant', pk=id)

    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid() and request.method == "POST":
        form.save()
        url = reverse('Homepage:restaurant') + f'?restaurant_name={restaurant.name}'
        return redirect(url)
    
    else:
        form = ReviewForm(instance=review)

    return render(request, "edit_review.html", {'form': form, 'review': review})

def delete_review(request, id):
    review = get_object_or_404(Review, pk=id)
    restaurant = review.restaurant

    # Pastikan hanya user yang membuat review bisa menghapusnya
    if review.user != request.user:
        return redirect('Homepage:restaurant', pk=id)
    review.delete()
    url = reverse('Homepage:restaurant') + f'?restaurant_name={restaurant.name}'
    return HttpResponseRedirect(url)

@csrf_exempt
@require_POST
def add_review_entry_ajax(request, restaurant_id):
    try:
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")
        user = request.user

        # Cek apakah restaurant_id ada dan restoran ditemukan
        restaurant = Restaurant.objects.get(id=restaurant_id)

        # Simpan review baru
        new_review = Review(
            comment=comment,
            rating=int(rating) if rating else 0,
            user=user,
            restaurant=restaurant
        )
        new_review.save()

        # Data review baru untuk dikembalikan ke AJAX
        review_data = {
            "user": user.username,
            "comment": comment,
            "rating": int(rating),
            "time": new_review.time.strftime("%Y-%m-%d"),
            "review_id": str(new_review.id)
        }
        
        reviews = restaurant.review.all()
        html = render_to_string('review_store_detail.html', {'reviews':reviews}, request=request)
        return JsonResponse({"status": "success", "html": html})

    except Restaurant.DoesNotExist:
        return JsonResponse({"status": "error", "errors": "Restaurant not found"}, status=404)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"status": "error", "errors": str(e)}, status=500)

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_review = Review.objects.create(
            user=request.user,
            comment=data["comment"],
            rating=int(data["rating"]),
        )

        new_review.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)