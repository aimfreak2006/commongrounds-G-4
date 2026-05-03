from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name']


class CustomProfileUpdateForm(ProfileUpdateForm):   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['display_name'].label = ''
        self.fields['display_name'].help_text = ''
        self.fields['display_name'].widget.attrs.update({
            'placeholder': 'Display Name'
        })


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomRegisterForm(RegisterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = ''
        self.fields['username'].help_text = '' 
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })

        self.fields['email'].label = ''
        self.fields['email'].help_text = '' 
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email'
        })

        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '' 
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })