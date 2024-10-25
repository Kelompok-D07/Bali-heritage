from django.urls import path
from Review.views import show_main, add_review_entry_ajax

app_name = 'Review'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-review-entry-ajax', add_review_entry_ajax, name='add_review_entry_ajax'),
]