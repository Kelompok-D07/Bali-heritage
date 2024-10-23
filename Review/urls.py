from django.urls import path
from Review.views import show_main

app_name = 'Review'

urlpatterns = [
    path('', show_main, name='show_main'),
]