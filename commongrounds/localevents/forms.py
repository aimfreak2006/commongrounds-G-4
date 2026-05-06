from django import forms
from .models import Event, EventSignup


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'category', 'event_image',
            'description', 'location', 'start_time',
            'end_time', 'event_capacity', 'status',
            ]


class CustomEventCreateForm(EventCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].label = ''
        self.fields['title'].help_text = ''
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Event Title'
        })

        self.fields['category'].label = ''
        self.fields['category'].help_text = ''
        self.fields['category'].widget.attrs.update({
            'placeholder': 'Event Category'
        })

        self.fields['description'].label = ''
        self.fields['description'].help_text = ''
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Event Description'
        })

        self.fields['location'].label = ''
        self.fields['location'].help_text = ''
        self.fields['location'].widget.attrs.update({
            'placeholder': 'Event Location'
        })

        self.fields['start_time'].label = ''
        self.fields['start_time'].help_text = ''
        self.fields['start_time'].widget.attrs.update({
            'placeholder': 'Event Start Time'
        })

        self.fields['end_time'].label = ''
        self.fields['end_time'].help_text = ''
        self.fields['end_time'].widget.attrs.update({
            'placeholder': 'Event End Time'
        })

        self.fields['event_capacity'].label = ''
        self.fields['event_capacity'].help_text = ''
        self.fields['event_capacity'].widget.attrs.update({
            'placeholder': 'Event Capacity'
        })


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'category', 'event_image',
            'description', 'location', 'start_time',
            'end_time', 'event_capacity', 'status',
            ]


class CustomEventUpdateForm(EventUpdateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].label = ''
        self.fields['title'].help_text = ''
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Event Title'
        })

        self.fields['category'].label = ''
        self.fields['category'].help_text = ''
        self.fields['category'].widget.attrs.update({
            'placeholder': 'Event Category'
        })

        self.fields['description'].label = ''
        self.fields['description'].help_text = ''
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Event Description'
        })

        self.fields['location'].label = ''
        self.fields['location'].help_text = ''
        self.fields['location'].widget.attrs.update({
            'placeholder': 'Event Location'
        })

        self.fields['start_time'].label = ''
        self.fields['start_time'].help_text = ''
        self.fields['start_time'].widget.attrs.update({
            'placeholder': 'Event Start Time'
        })

        self.fields['end_time'].label = ''
        self.fields['end_time'].help_text = ''
        self.fields['end_time'].widget.attrs.update({
            'placeholder': 'Event End Time'
        })

        self.fields['event_capacity'].label = ''
        self.fields['event_capacity'].help_text = ''
        self.fields['event_capacity'].widget.attrs.update({
            'placeholder': 'Event Capacity'
        })


class EventSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['new_registrant']
        labels = {
            'new_registrant': 'Your Full Name',
            }
