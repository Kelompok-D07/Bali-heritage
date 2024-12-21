from django.urls import path
from bookmarks.views import delete_bookmarks_flutter, edit_notes_flutter, show_bookmarks,delete_bookmarks_item,edit_notes, add_to_bookmarks, filter_bookmarks, show_json, toggle_bookmark

app_name = 'bookmarks'

urlpatterns = [
    path('', show_bookmarks, name='show_bookmarks'),
    path('delete-bookmarks-item/<int:item_id>/', delete_bookmarks_item, name='delete_bookmarks_item'),
    path('edit-notes/<int:item_id>/', edit_notes, name='edit_notes'),
    path('update_bookmarks/', add_to_bookmarks, name='update_bookmarks'),
    path('filter/', filter_bookmarks, name='filter_bookmarks'),  # URL untuk filtering

    # Flutter
    path('json/', show_json, name='show_json'),
    path('edit-notes/', edit_notes_flutter, name='edit_notes_flutter'),
    path('delete-bookmarks-flutter/<str:product_name>/', delete_bookmarks_flutter, name='delete_bookmarks_flutter'),
    path('toogle-bookmark/', toggle_bookmark, name='toggle_bookmark'),
]