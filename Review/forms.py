from django.forms import ModelForm, HiddenInput 
from Review.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widget = {
            'restaurant': HiddenInput(),
        }