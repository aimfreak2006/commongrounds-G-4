from django import forms
from .models import ProjectReview, ProjectRating


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment', 'image']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 10, 'placeholder': '1-10'}),
        }