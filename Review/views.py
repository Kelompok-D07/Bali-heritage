from django.shortcuts import render, redirect, reverse, get_object_or_404
from Review.models import Review
from Review.forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

@login_required(login_url='/')
def show_main(request):
    review = Review.objects.filter(user=request.user)
    context = {
        'review': review,
    }

    return render(request, "main.html", context)

def create_review_entry(request):
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.user = request.user
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "review.html", context)

def review_store_detail(request, id):
    # Ambil review yang terkait dengan store tertentu
    reviews = Review.objects.filter(pk=id)
    return render(request, 'review_store_detail.html', {'reviews': reviews})

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

    # Pastikan hanya user yang menulis review bisa mengeditnya
    if review.user != request.user:
        return redirect('review_store_detail', pk=review.id)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form = ReviewForm(request.POST or None, instance=review)
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    
    else:
        form = ReviewForm(instance=review)

    return render(request, "edit_review.html", {'form': form, 'review': review})

def delete_review(request, id):
    review = get_object_or_404(Review, pk=id)

    # Pastikan hanya user yang membuat review bisa menghapusnya
    if review.user != request.user:
        return redirect('review_store_detail', pk=review.id)

    if request.method == 'POST':
        review.delete()
        return redirect('review_store_detail', pk=review.id)

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