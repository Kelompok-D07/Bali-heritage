from django.urls import path
from Review.views import show_main, create_review_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, add_review_entry_ajax, review_store_detail, edit_review, delete_review, create_review_flutter

app_name = 'review'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-review-entry/<uuid:restaurant_id>/', create_review_entry, name='create_review_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('add-review-entry-ajax/<uuid:restaurant_id>/', add_review_entry_ajax, name='add_review_entry_ajax'),
    path('store/<str:id>/', review_store_detail, name='review_store_detail'),
    path('edit-review/<uuid:id>/', edit_review, name='edit_review'),
    path('delete-review/<uuid:id>/', delete_review, name='delete_review'),
    path('create-review-flutter/', create_review_flutter, name='create_review_flutter'),
]