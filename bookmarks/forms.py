from django import forms
from .models import Bookmark

class EditNotesForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['notes']
        widgets = {
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Edit your notes'}),
        }
        labels = {
            'notes': 'Edit Notes',
        }