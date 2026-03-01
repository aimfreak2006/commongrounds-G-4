from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import EventType, Event

# Create your views here.

class EventListView(ListView):
    model = EventType
    template_name = "localevents/event_list.html"

class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_details.html"