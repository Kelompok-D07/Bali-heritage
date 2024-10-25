from django.shortcuts import render
from Review.models import Review
from Review.forms import ReviewForm

def show_main(request):
    context = {
        'name': 'name',
        'description': 'Hello'
    }

    return render(request, "main.html", context)
