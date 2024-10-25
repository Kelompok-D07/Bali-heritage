from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('forum/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('forum/new/', views.forum_create, name='forum_create'),
    path('forum/<int:pk>/like/', views.forum_like, name='forum_like'),
]
