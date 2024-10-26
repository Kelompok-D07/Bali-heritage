from django.urls import path
from Homepage.views import show_main, restaurant, filter_product

app_name = 'Homepage'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('restaurant/', restaurant, name='restaurant'),
    path('filter-product/', filter_product, name='filter_products')  # URL untuk filtering
]