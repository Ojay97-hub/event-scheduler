from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView, DetailView
from .models import Event, Registration
from .forms import EventForm, CustomUserCreationForm, EventRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here. 
class EventsList(generic.ListView):
    model = Event 
    template_name = 'events/event_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category', '')
        date_start = self.request.GET.get('date_start', '')
        date_end = self.request.GET.get('date_end', '')
        price_min = self.request.GET.get('price_min', '')
        price_max = self.request.GET.get('price_max', '')
        free_only = self.request.GET.get('free', '')

        # filter by category
        if category:
            queryset = queryset.filter(category=category)  # Filter by category if provided
        # filter by price
        if price_min:
            try:
                queryset = queryset.filter(price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                queryset = queryset.filter(price__lte=float(price_max))
            except ValueError:
                pass 
        # filter by free
        if free_only:
            queryset = queryset.filter(price__isnull=True)
        # filter by dates
        if date_start:
            queryset = queryset.filter(date__gte=date_start)  # Filter for events on or after the start date
        if date_end:
            queryset = queryset.filter(date__lte=date_end)  # Filter for events on or before the end date
        
        return queryset.distinct()

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
        event_id = self.kwargs.get('pk') 
        return get_object_or_404(Event, id=event_id)

@login_required
def create_event(request):
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
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if Registration.objects.filter(user=request.user, event=event).exists():
                messages.warning(request, 'You are already registered for this event.')
            elif event.capacity <= event.registrations.count():
                messages.warning(request, 'This event has reached its capacity.')
            else:
                # Save registration and send email
                Registration.objects.create(user=request.user, event=event)
                
                # Send confirmation email
                send_mail(
                    subject=f"Registration Confirmation for {event.title}",
                    message=f"Thank you for registering for {event.title} on {event.date} at {event.time}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )

                messages.success(request, 'You have successfully registered for the event! A confirmation email has been sent.')
                return redirect('Event_List')
    else:
        form = EventRegistrationForm()

    return render(request, 'events/event_detail.html', {'event': event, 'form': form})

# Unregister from an event
@login_required
def unregister_from_event(request, event_id):
    # Get the event object
    event = get_object_or_404(Event, id=event_id)
    
    # Get the registration object directly, or raise a 404 if it doesn't exist
    registration = get_object_or_404(Registration, user=request.user, event=event)

    # Delete the registration
    registration.delete()
    messages.success(request, 'You have successfully unregistered from the event.')

    return redirect('registered_events')

@login_required
def registered_events(request):
    # Get all events the user is registered for
    registered_events = Registration.objects.filter(user=request.user)
    
    return render(request, 'events/registered_events.html', {'registered_events': registered_events})
