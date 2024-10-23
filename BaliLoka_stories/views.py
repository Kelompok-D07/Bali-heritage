from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'name',
        'description': 'Hello'
    }

    return render(request, "main.html", context)
