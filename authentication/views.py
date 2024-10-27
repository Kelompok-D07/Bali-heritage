from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already exists."})
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        response = JsonResponse({"success": True})
        response.set_cookie("auth", "true")
        return response

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            response = JsonResponse({"success": True})
            response.set_cookie("auth", "true")
            return response
        else:
            return JsonResponse({"success": False, "error": "Invalid credentials."})

@csrf_exempt
def logout_user(request):
    logout(request)
    response = JsonResponse({"success": True})
    response.delete_cookie("auth")
    return response