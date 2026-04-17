from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name']


class RegisterForm(UserCreationForm):
    display_name = forms.CharField(max_length=63)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=Profile._meta.get_field('role').choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
