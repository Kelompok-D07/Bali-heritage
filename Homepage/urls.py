from django.urls import path
from Homepage.views import show_main, restaurant

app_name = 'Homepage'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('restaurant/', restaurant, name='restaurant'),
]