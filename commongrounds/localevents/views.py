from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import EventType, Event, EventSignup
from django.shortcuts import redirect
# from accounts.mixins import RoleRequiredMixin



# def EventListView(request):
#     user_events = Event.objects.filter(maker=request.user.profile)
#     other_events = Event.objects.exclude(maker=request.user.profile)
#     ctx = {
#         "user_events": user_events,
#         "other_events": other_events,
#     }
#     if (request.method == "POST"):

#     return render(request, "localevents/event_list.html", ctx)


# def EventDetailView(request, pk):
#     event = Event.objects.get(pk=pk)
#     ctx = { "event": event }
#     return render(request, "localevents/event_detail.html", ctx)


# def EventCreateView(request):
#     event = Event.objects.get()
#     ctx = { "event" : event }


# def EventUpdateView(request, pk):



# def EventSignupFormView(request):

class EventListView(ListView):
    model = Event
    template_name = "localevents/event_list.html"
    context_object_name = "events"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_events = Event.objects.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            contributed = Event.objects.filter(contributor=profile)

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_detail.html"
    context_object_name = "event"


class EventCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Event
    template_name = "localevents/event_create.html"
    context_object_name = ""


class EventUpdateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Event
    template_name = "localevents/event_update.html"
    context_object_name = ""


class EventSignupView(EventCreateView):
    model = EventSignup
    template_name = "localevents/event_signup.html"
    context_object_name = ""