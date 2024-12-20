from django.urls import path
from Homepage.views import show_main, restaurant, filter_product,create_product_flutter, get_categories, get_restaurants

app_name = 'Homepage'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('restaurant/', restaurant, name='restaurant'),
    path('filter-product/', filter_product, name='filter_products'),  # URL untuk filtering
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),
    path('get-categories/', get_categories, name='get_categories'),
    path('get-restaurants/', get_restaurants, name='get_restaurants'),
]