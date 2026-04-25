from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventSignupFormView

urlpatterns = [
    path('events/', EventListView, name='event_list'),
    path('event/<int:pk>', EventDetailView, name='event_detail'),
    path('event/add', EventCreateView, name='event_create'),
    path('event/<int:pk>/edit', EventUpdateView, name='event_update'),
    path('event/<int:pk>/signup', EventSignupFormView, name='event_signup'),
]

app_name = "localevents"
