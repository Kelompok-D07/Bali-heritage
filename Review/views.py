from django.shortcuts import render
from Review.models import Review
from Review.forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

@login_required
def show_main(request):
    context = {
        'name': 'name',
        'description': 'Hello'
    }

    return render(request, "main.html", context)

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