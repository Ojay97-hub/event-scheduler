from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView, DetailView
from .models import Event, Registration, Location
from .forms import EventForm, LocationForm, CustomUserCreationForm, EventRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Value, DateTimeField, Exists, OuterRef, Prefetch
from django.db.models.functions import Concat
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class EventsList(generic.ListView):
    model = Event
    template_name = 'events/event_list.html'

    def get_queryset(self):
        # Get the base queryset filtered by current or future events
        queryset = super().get_queryset().filter(start_date__gte=timezone.now().date())

        # Retrieve filters from query parameters
        category = self.request.GET.get('category', '')
        date_start = self.request.GET.get('date_start', '')
        date_end = self.request.GET.get('date_end', '')
        price_min = self.request.GET.get('price_min', '')
        price_max = self.request.GET.get('price_max', '')
        free_only = self.request.GET.get('free', '')
        organiser_id = self.request.GET.get('organiser', '')
        is_online = self.request.GET.get('is_online', '')
        is_in_person = self.request.GET.get('is_in_person', '')

        # Apply category filter
        if category:
            queryset = queryset.filter(category=category)

        # Apply organiser filter
        if organiser_id:
            queryset = queryset.filter(organiser_id=organiser_id)

        # Apply price filters
        if price_min:
            try:
                queryset = queryset.filter(price__gte=float(price_min))
            except ValueError:
                messages.error(self.request, "Invalid minimum price value.")

        if price_max:
            try:
                queryset = queryset.filter(price__lte=float(price_max))
            except ValueError:
                messages.error(self.request, "Invalid maximum price value.")

        # Apply free event filter
        if free_only:
            queryset = queryset.filter(free=True)

        # Apply online and in-person filters
        if is_online and not is_in_person:
            queryset = queryset.filter(location__is_online=True)
        elif is_in_person and not is_online:
            queryset = queryset.filter(location__is_online=False)

        # Apply date filters
        if date_start:
            try:
                date_start = timezone.datetime.strptime(date_start, "%Y-%m-%d").date()
                queryset = queryset.filter(start_date__gte=date_start)
            except ValueError:
                messages.error(self.request, "Invalid start date format.")

        if date_end:
            try:
                date_end = timezone.datetime.strptime(date_end, "%Y-%m-%d").date()
                queryset = queryset.filter(end_date__lte=date_end)
            except ValueError:
                messages.error(self.request, "Invalid end date format.")

        # Annotate and order events by their start datetime
        queryset = queryset.annotate(
            start_datetime=Concat('start_date', Value(' '), 'start_time', output_field=DateTimeField())
        ).order_by('start_datetime').distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Current date and time
        today = timezone.now().date()  # Use only the date part
        current_time = timezone.now().time()  # Full current time

        # Calculate whether each event is in the past
        for event in context['object_list']:
            # Ensure we're comparing the date part only
            if isinstance(event.end_date, datetime):  # If it's a datetime object, we need to extract the date part
                event_end_date = event.end_date.date()  # Convert to date part only
            else:
                event_end_date = event.end_date  # It's already a date object

            event.is_past = (
                event_end_date < today or  # Event end date has passed
                (event_end_date == today and event.end_time <= current_time)  # Event ends today and time has passed
            )

        # Add additional context for category choices, today, and current time
        context['category_choices'] = Event.CATEGORY_CHOICES
        context['today'] = today
        context['now'] = timezone.now()  # Keep the full datetime for any further comparisons or views

        # Registered events for the authenticated user
        if self.request.user.is_authenticated:
            registered_event_ids = Registration.objects.filter(user=self.request.user).values_list('event__id', flat=True)
            context['registered_events'] = list(registered_event_ids)

        context['today'] = timezone.now()

        # Get a list of users who are organisers
        organisers = User.objects.filter(events__isnull=False).distinct()
        context['organisers'] = organisers

        # Organiser status for each event
        context['organiser_status_by_event'] = {event.id: (event.organiser == self.request.user) for event in context['object_list']}

        return context

# Event detail view 
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        event_id = self.kwargs.get('pk')
        return get_object_or_404(Event, id=event_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventRegistrationForm()  # Registration form for the event
        context['is_registered'] = Registration.objects.filter(user=self.request.user, event=self.object).exists() if self.request.user.is_authenticated else False

        # Get the current date and time
        today = timezone.localtime(timezone.now()) 

        # Combine event start date and start time into a single datetime object and make it timezone-aware
        event_start_datetime = timezone.make_aware(datetime.combine(self.object.start_date, self.object.start_time))

        # Check if the event has already taken place
        context['event_has_taken_place'] = event_start_datetime <= today

        # Add data to context
        context['form'] = EventRegistrationForm()  # Include the registration form if needed
        return context

@login_required
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        location_form = LocationForm(request.POST)

        print("Debug: EventForm data:", event_form.data)
        print("Debug: LocationForm data:", location_form.data)

        if event_form.is_valid() and location_form.is_valid():
            print("Debug: Both forms are valid.")
            # Save the location first
            location = location_form.save()
            # Now create the event with the saved location
            event = event_form.save(commit=False)
            event.location = location
            event.organiser = request.user
            event.save()
            print("Debug: Event saved successfully.")
            return redirect('created_events')  # Adjust the redirect as needed

        # Print errors for debugging
        print("Debug: EventForm errors:", event_form.errors)
        print("Debug: LocationForm errors:", location_form.errors)

    else:
        event_form = EventForm()
        location_form = LocationForm()

    context = {
        'event_form': event_form,
        'location_form': location_form,
    }
    return render(request, 'events/create_event.html', context)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Only allow the organiser to edit the event
    if request.user != event.organiser:
        messages.error(request, "You are not authorized to edit this event.")
        return redirect('event_detail', pk=event.id)

    if request.method == 'POST':
        print("Debug: POST request received.")

        event_form = EventForm(request.POST, instance=event)
        location_form = LocationForm(request.POST, instance=event.location)

        print(f"Debug: EventForm data: {event_form.data}")
        print(f"Debug: LocationForm data: {location_form.data}")

        if event_form.is_valid() and location_form.is_valid():
            print("Debug: Both forms are valid.")

            # Save the location first
            location = location_form.save()
            print(f"Debug: Updated location: {location}")

            # Save the event
            event = event_form.save(commit=False)
            event.location = location
            event.save()
            print(f"Debug: Updated event: {event}")

            messages.success(request, "Event updated successfully.")
            print(f"Debug: Redirecting to event_detail with pk={event.id}")
            return redirect('event_detail', pk=event.id)
        else:
            print("Debug: EventForm errors:", event_form.errors)
            print("Debug: LocationForm errors:", location_form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        print("Debug: GET request received.")

        event_form = EventForm(instance=event)
        location_form = LocationForm(instance=event.location)

    return render(request, 'events/edit_event.html', {
        'form': event_form,
        'location_form': location_form,
        'event': event,
    })


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organiser=request.user)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('created_events')  # Redirect to the page where they can see their created events

    return redirect('event_detail', pk=event.id)

@login_required
def created_events_view(request):
    events = Event.objects.filter(organiser=request.user)
    return render(request, 'events/created_events.html', {'events': events})


# Register as event user or event organiser
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            user_type = form.cleaned_data['user_type']  # Get user_type from form data

            # Get the appropriate group based on user type
            try:
                group = Group.objects.get(name=user_type.replace('_', ' ').title())
                user.groups.add(group)  # Add the user to the selected group
            except Group.DoesNotExist:
                messages.error(request, 'User type group does not exist.')
                return redirect('signup')

            login(request, user)  # Log in the user
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

# Ensure only organisers or admins can access this view
@login_required
def organiser_events(request, organiser_id):
    # Get the organiser object
    organiser = get_object_or_404(User, id=organiser_id)

    # Check if the logged-in user is the organiser, or an admin (staff member)
    if request.user != organiser and not request.user.is_staff:
        messages.warning(request, "You are not allowed to view this organiser's events.")
        return redirect('event_list')  # Redirect to the event list if the user is not the organiser

    # Get all events by this organiser
    events = Event.objects.filter(organiser=organiser)

    # Get the current date and time to check registration status
    today = timezone.now()

    # Render the organiser's page with events
    return render(request, 'events/view_organiser.html', {
        'organiser': organiser,
        'events': events,
        'today': today
    })

# Registration view for events
@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Prevent organisers from registering for events
    if request.user == event.organiser:
        messages.warning(request, "Organisers cannot register for their own events.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the user is already registered for this event
            if Registration.objects.filter(user=request.user, event=event).exists():
                messages.warning(request, 'You are already registered for this event.')
                return redirect('event_list')

            # Check if the event is full
            if event.capacity <= event.registrations.count():
                messages.warning(request, 'This event has reached its capacity.')
                return redirect('event_list')

            # Create a new registration
            registration = Registration(user=request.user, event=event)

            try:
                # Validate the registration (this will raise a ValidationError if invalid)
                registration.clean()  # Validation on model level
                registration.save()  # Save the registration

                # Send confirmation email
                send_mail(
                    subject=f"Registration Confirmation for {event.title}",
                    message=f"Thank you for registering for {event.title} on {event.start_date} at {event.start_time}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                messages.success(request, 'You have successfully registered for the event! A confirmation email has been sent.')
                return redirect('event_list')  # Redirect after successful registration

            except ValidationError as e:
                messages.error(request, str(e))  # Show validation error
            except Exception as e:
                messages.error(request, 'Registration successful, but failed to send confirmation email.')

    else:
        form = EventRegistrationForm()

    # Check if user is already registered for the event
    is_registered = Registration.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'form': form,
        'is_registered': is_registered
    })


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

    # Get the current date and time
    now = timezone.now()

    # Separate into upcoming and past events
    upcoming_events = [
        registration for registration in registered_events 
        if registration.event.start_date >= now
    ]
    past_events = [
        registration for registration in registered_events 
        if registration.event.start_date < now
    ]

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    return render(request, 'events/registered_events.html', context)

# organiser access to registered attendees
@login_required
def attendee_list(request, event_id):
    # Get the event and ensure the user is the organizer
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organiser:
        # Show a warning message and redirect
        messages.warning(request, "You are not authorized to view the attendees for this event.")
        return redirect('event_list')

    # Retrieve attendees registered for the event
    attendees = Registration.objects.filter(event=event).select_related('user')

    context = {
        'event': event,
        'attendees': attendees,
    }
    return render(request, 'events/attendee_list.html', context)