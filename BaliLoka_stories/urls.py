from django.urls import path
from BaliLoka_stories.views import show_stories, create_stories_entry, show_xml, show_json, add_stories_entry_ajax, edit_stories, delete_stories


app_name = 'BaliLoka_stories'

urlpatterns = [
    path('', show_stories, name='show_stories'),
    path('create-stories-entry', create_stories_entry, name='create_stories_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('create-stories-entry-ajax', add_stories_entry_ajax, name='add_stories_entry_ajax'),
    path('edit-stories/<uuid:id>', edit_stories, name='edit_stories'),
    path('delete/<uuid:id>', delete_stories, name='delete_stories'),
]