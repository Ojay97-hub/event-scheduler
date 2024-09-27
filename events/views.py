from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView
from .models import Event
from .forms import EventForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group

# Create your views here. 
class EventsList(generic.ListView):
    queryset = Event.objects.all()  # Can add filter queryset to show only published events 
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

# Register as event user or event organiser following stackoverflow guidance
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            user_type = form.cleaned_data['user_type']  # Get user_type from form data

            # Get the appropriate group based on user type
            if user_type == 'event_user':
                group = Group.objects.get(name='Event User')
            else:
                group = Group.objects.get(name='Event Organiser')

            user.groups.add(group)  # Add the user to the selected group
            login(request, user)  # Log in the user
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})
