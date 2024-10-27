from django.urls import path
from .views import forum_list, create_post, like_post

app_name = 'Forum'

urlpatterns = [
    path('', forum_list, name='forum_list'),
    path('create/', create_post, name='create_post'),
    path('like/<int:post_id>/', like_post, name='like_post'),
]
