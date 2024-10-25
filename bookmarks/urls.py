from django.urls import path
from bookmarks.views import show_bookmarks,delete_bookmarks_item,edit_notes

app_name = 'bookmarks'

urlpatterns = [
    path('', show_bookmarks, name='show_bookmarks'),
    path('delete-bookmarks-item/<int:item_id>/', delete_bookmarks_item, name='delete_bookmarks_item'),
    path('edit-notes/<int:item_id>/', edit_notes, name='edit_notes'),
]