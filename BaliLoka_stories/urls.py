from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from BaliLoka_stories.views import show_stories, create_stories_entry, show_xml, show_json, add_stories_entry_ajax, edit_stories, delete_stories, create_stories_flutter


app_name = 'BaliLoka_stories'

urlpatterns = [
    path('', show_stories, name='show_stories'),
    path('create-stories-entry', create_stories_entry, name='create_stories_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('add-stories-entry-ajax', add_stories_entry_ajax, name='add_stories_entry_ajax'),
    path('edit-stories/<uuid:id>', edit_stories, name='edit_stories'),
    path('delete-stories/<uuid:id>', delete_stories, name='delete_stories'),
    path('create-flutter/', create_stories_flutter, name='create_stories_flutter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)