from django.urls import path
from BaliLoka_stories.views import show_main

app_name = 'BaliLoka_stories'

urlpatterns = [
    path('', show_main, name='show_main'),
]