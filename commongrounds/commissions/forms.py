from django import forms
from .models import Commission, CommissionType, Job


class CommissionForm(forms.ModelForm):
    title = forms.CharField(
        label="Commission Title",
        max_length=255,
        required=False
    )
    description = forms.CharField(widget=forms.Textarea, required=False)
    type = forms.ModelChoiceField(
        label="Commission Type",
        queryset=CommissionType.objects.all(),
        required=False
    )
    status = forms.ChoiceField(
        label="Status",
        choices=Commission.Status.choices
    )
    people_required = forms.IntegerField(min_value=0, required=False)

    class Meta:
        model = Commission
        fields = ['title', 'description', 'type', 'people_required', 'status']


class JobForm(forms.ModelForm):
    role = forms.CharField(
        label="Job Role",
        max_length=255
    )
    manpower_required = forms.IntegerField(min_value=0)

    class Meta:
        model = Job
        fields = ['role', 'manpower_required']


class JobApplicationForm(forms.ModelForm):
    job = forms.ModelChoiceField
