from django.shortcuts import render
from .models import EventType, Event

def EventListView(request):
    events = Event.objects.all().order_by('created_on')
    event_type = EventType.objects.all().order_by('name')
    ctx = {
        "events" : events,
        "categories" : event_type,
    }
    return render(request, "localevents/event_list.html", ctx)

def EventDetailView(request, pk):
    event = Event.objects.get(pk=pk)
    ctx = { "event" : event }
    return render(request, "localevents/event_detail.html", ctx)