from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView, DetailView
from .models import Event, Registration
from .forms import EventForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

# Create your views here. 
class EventsList(generic.ListView):
    model = Event 
    template_name = 'events/event_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category=category)  # Filter by category if provided
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Event.CATEGORY_CHOICES
        return context

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'  
    
    def get_object(self, queryset=None):
        # Get the 'id' from the URL and use it to retrieve the object
        return get_object_or_404(Event, id=self.kwargs['id'])

@login_required
def create_event(request):
    # This check is still required to enforce permission for Event Organisers
    if request.user.groups.filter(name='Event Organiser').exists():
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.organiser = request.user
                event.save()
                messages.success(request, 'Event created successfully!')
                return redirect('Event_Page')
        else:
            form = EventForm()

        return render(request, 'events/create_event.html', {'form': form})

    else:
        messages.error(request, 'You do not have permission to create an event.')
        return redirect('home') 

# Register as event user or event organiser
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
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

# Registration view for events
@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        if Registration.objects.filter(user=request.user, event=event).exists():
            messages.warning(request, 'You are already registered for this event.')
        elif event.capacity <= event.registrations.count():
            messages.warning(request, 'This event has reached its capacity.')
        else:
            Registration.objects.create(user=request.user, event=event)
            messages.success(request, 'You have successfully registered for the event!')
            return redirect('Event_Page')

    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def registered_events(request):
    # Get all events the user is registered for
    registered_events = Registration.objects.filter(user=request.user)
    
    return render(request, 'events/registered_events.html', {'registered_events': registered_events})
