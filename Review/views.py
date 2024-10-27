from django.shortcuts import render, redirect, reverse, get_object_or_404
from Review.models import Review
from Review.forms import ReviewForm
from Homepage.models import Restaurant
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

@login_required(login_url='/')
def show_main(request):
    review = Review.objects.filter(user=request.user)
    context = {
        'review': review,
    }

    return render(request, "main.html", context)

from uuid import UUID

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
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Review.objects.all()
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
def add_review_entry_ajax(request):
    comment = request.POST.get("comment")
    rating = request.POST.get("rating")
    user = request.user

    new_review = Review(
        comment=comment,
        rating=rating,
        user=user
    )
    new_review.save()

    return HttpResponse(b"CREATED", status=201)