from django.shortcuts import render, redirect
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