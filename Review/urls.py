from django.urls import path
from Review.views import show_main, create_review_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, add_review_entry_ajax

app_name = 'Review'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-review-entry', create_review_entry, name='create_review_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('add-review-entry-ajax', add_review_entry_ajax, name='add_review_entry_ajax'),
]