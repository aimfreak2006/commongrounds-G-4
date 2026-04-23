from django import forms
from accounts.models import Profile
from .models import Commission, CommissionType

class CommissionForm(forms.ModelForm):
    title = forms.CharField(
        label="Commission Title",
        max_length=255
    )
    description = forms.TextInput()
    type = forms.ModelChoiceField(
        label="Commission Type",
        queryset=CommissionType.objects.all()
    )
    people_required = forms.IntegerField()

    class Meta:
        model = Commission
        fields = '__all__'
