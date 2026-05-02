from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Event, EventSignup
from .forms import EventSignupForm, EventCreateForm, EventUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


class EventListView(ListView):
    model = Event
    template_name = "localevents/event_list.html"
    context_object_name = "events"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_events = Event.objects.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            organized = Event.objects.filter(organizer=profile)
            signed_up = Event.objects.filter(event_signups__user_registrant=profile)

            grouped_pks = (
                organized.values('pk') |
                signed_up.values('pk')
            )

            context['organized_events'] = organized
            context['signed_up_events'] = signed_up
            context['all_events'] = all_events.exclude(pk__in=grouped_pks)

        else:
            context['all_events'] = all_events

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_detail.html"
    context_object_name = "event"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user
        current_signups = EventSignup.objects.filter(event=event).count()

        if current_signups >= event.event_capacity:
            context['is_full'] = True

        if user.is_authenticated:
            context['is_organizer'] = (event.organizer == user.profile)
            context['is_signed_up'] = EventSignup.objects.filter(
                event=event,
                user_registrant=user.profile
            ).exists()

        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('event_signup', pk=self.get_object().pk)
        
        event = self.get_object()

        if EventSignup.objects.filter(event=event).count() >= event.event_capacity:
            messages.error(request, "This event is full.")
        else:
            EventSignup.objects.get_or_create(
                event=event,
                user_registrant=request.user
            )
            messages.success(request, "Thank you for signing up.")
        
        return redirect('event_detail', pk=event.pk)


class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    template_name = "localevents/event_create.html"
    form_class = EventCreateForm
    context_object_name = "create_form"

    def test_func(self):
        return self.request.user.profile.role == 'Event Organizer'
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user.profile
        return super().form_valid(form)



class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = "localevents/event_update.html"
    form_class = EventUpdateForm
    context_object_name = "update_form"

    def test_func(self):
        profile = self.request.user.profile
        return profile.role == "Event Organizer" and self.get_object().organizer == profile

class EventSignupView(CreateView):
    model = EventSignup
    template_name = "localevents/event_signup.html"
    form_class = EventSignupForm

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])

        current_count = EventSignup.objects.filter(event=event).count()
        if current_count >= event.event_capacity:
            messages.error(self.request, "This event is now full.")
            return redirect('localevents:event_detail', pk=event.pk)
        
        form.instance.event = event

        if self.request.user.is_authenticated:
            form.instance.user_registrant = self.request.user.profile
            if not form.cleaned_data.get('new_registrant'):
                form.instance.new_registrant = self.request.user.get_full_name()

        response = super().form_valid(form)
        event.save()

        messages.success(self.request, "Thank you for signing up.")
        return response
    
    def get_success_url(self):
        return reverse('localevents:event_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['pk'])
        return context
    