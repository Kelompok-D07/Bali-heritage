from django.urls import path
from bookmarks.views import show_bookmarks,delete_bookmarks_item

app_name = 'bookmarks'

urlpatterns = [
    path('', show_bookmarks, name='show_bookmarks'),
    path('delete-bookmarks-item/<int:item_id>/', delete_bookmarks_item, name='delete_bookmarks_item'),
]