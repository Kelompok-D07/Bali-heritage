from django.forms import ModelForm
from BaliLoka_stories.models import StoriesEntry

class StoriesEntryForm(ModelForm):
    class Meta:
        model = StoriesEntry
        fields = ["name", "image", "description"]