from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('create/', views.create_post, name='create_post'),
]
