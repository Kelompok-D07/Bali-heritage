from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'User',
        'description': 'Hello'
    }

    return render(request, "main.html", context)