# forum/urls.py

from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('like/<str:post_id>/', views.like_post, name='like_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('get_post/<str:post_id>/', views.get_post, name='get_post'),
    path('edit_post/<str:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<str:post_id>/', views.delete_post, name='delete_post'),
    path('restaurant_search/', views.restaurant_search, name='restaurant_search'),
]
