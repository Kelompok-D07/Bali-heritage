from django.urls import path
from Homepage.views import show_main, restaurant, filter_product, get_categories, get_restaurants, get_products, create_product_flutter

app_name = 'Homepage'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('restaurant/', restaurant, name='restaurant'),
    path('filter-product/', filter_product, name='filter_products'),  # URL untuk filtering
    path('get-categories/', get_categories, name='get_categories'),
    path('get-restaurants/', get_restaurants, name='get_restaurants'),
    path('get-products/', get_products, name='get_products'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),

]