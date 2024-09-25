from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView
from .models import Event
from .forms import EventForm

# Create your views here. 
class EventsList(generic.ListView):
    queryset = Event.objects.all() # can add filter queryset to status 1 to show only published events 
    template_name = "events/event_list.html"
    paginate_by = 6

class HomeView(TemplateView):
    template_name = 'home.html' 

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Event_Page')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})