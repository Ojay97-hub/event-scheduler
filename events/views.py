from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView
from .models import Event, Registration
from .forms import EventForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

# Create your views here. 
class EventsList(generic.ListView):
    queryset = Event.objects.all()  # Can add filter queryset to show only published events 
    # template_name = "events/event_list.html"
    paginate_by = 6

class HomeView(TemplateView):
    template_name = 'home.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user is in the 'Event Organiser' group
        context['is_event_organiser'] = self.request.user.groups.filter(name='Event Organiser').exists() if self.request.user.is_authenticated else False
        return context

@login_required
def create_event(request):
    # Check if the user is in the 'Event Organiser' group
    if request.user.groups.filter(name='Event Organiser').exists():
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('Event_Page')
        else:
            form = EventForm()

        return render(request, 'create_event.html', {'form': form})

    # If user is not an event organiser, redirect them or show an error
    else:
        return redirect('home') 

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

# registration view
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if Registration.objects.filter(user=request.user, event=event).exists():
                messages.warning(request, 'You are already registered for this event.')
            elif event.capacity <= event.registrations.count():
                messages.warning(request, 'This event has reached its capacity.')
            else:
                Registration.objects.create(user=request.user, event=event)
                messages.success(request, 'You have successfully registered for the event!')
                return redirect('Event_Page')
        else:
            messages.warning(request, 'You need to be logged in to register for an event.')

    return render(request, 'events/event_detail.html', {'event': event})

