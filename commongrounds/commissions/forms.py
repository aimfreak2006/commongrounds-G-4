from django import forms
from accounts.models import Profile
from .models import Commission, CommissionType, Job

class CommissionForm(forms.ModelForm):
    title = forms.CharField(
        label="Commission Title",
        max_length=255
    )
    description = forms.CharField(widget=forms.Textarea)
    type = forms.ModelChoiceField(
        label="Commission Type",
        queryset=CommissionType.objects.all()
    )
    
    people_required = forms.IntegerField()

    class Meta:
        model = Commission
        fields = ['title', 'description', 'type', 'people_required']


class JobForm(forms.ModelForm):
    role = forms.CharField(
        label="Job Role",
        max_length=255
    )
    manpower_required = forms.IntegerField()

    class Meta:
        model = Job
        fields = ['role', 'manpower_required']
            