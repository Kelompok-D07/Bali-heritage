from django import forms
from .models import Bookmark;

class AddToBookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['notes']  # Hanya catatan yang bisa ditambahkan
