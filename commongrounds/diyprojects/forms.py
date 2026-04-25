from django import forms
from .models import ProjectReview, ProjectRating


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        # We only include 'comment' and 'image' because 'project' and 'reviewer' 
        # will be set automatically in the view (using the logged-in user).
        fields = ['comment', 'image']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        # We only include 'score' because 'project' and 'profile' 
        # will be set automatically in the view.
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 10, 'placeholder': '1-10'}),
        }