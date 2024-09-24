from django.shortcuts import render
from django.views import generic
from .models import Event

# Create your views here.
class EventsList(generic.ListView):
    queryset = Event.objects.all() # can add filter queryset to status 1 to show only published events 
    template_name = "events/index.html"
    paginate_by = 6
