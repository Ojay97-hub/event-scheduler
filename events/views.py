from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView
from .models import Event

# Create your views here.
class EventsList(generic.ListView):
    queryset = Event.objects.all() # can add filter queryset to status 1 to show only published events 
    template_name = "events/event_list.html"
    paginate_by = 6

class HomeView(TemplateView):
    template_name = 'home.html' 