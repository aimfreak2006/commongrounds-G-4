from django.urls import path
from .views import EventListView, EventDetailView

urlpatterns = [
    path('events/', EventListView, name='event_list'),
    path('event/<int:pk>', EventDetailView, name='event_detail'),
]

app_name = "localevents"