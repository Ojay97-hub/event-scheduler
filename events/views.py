# Library imports
from datetime import datetime
import json

# Third-party imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import (
    Value, DateTimeField, Exists, OuterRef,
    Prefetch, Count, F, Case, When, BooleanField)
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Local imports
from .models import Event, Registration, Location
from .forms import (
    EventForm,
    LocationForm,
    CustomUserCreationForm,
    EventRegistrationForm,
)


# Create your views here.
class HomeView(TemplateView):
    """
    Displays the home page of the website.

    **Context**
    - No additional context variables.

    **Template**
    - `home.html`
    """
    template_name = 'home.html'


class EventsList(generic.ListView):
    """
    Displays a paginated list of upcoming events
    with various filtering options.

    **Model**
    - Displays data from the `Event` model.

    **Context**
    - `object_list`: A list of filtered and paginated `Event` instances.
    - `category_choices`: Event category choices from the `Event` model.
    - `today`: Current date.
    - `now`: Current date and time.
    - `registered_events`: List of event IDs that the authenticated user is
      registered for.
    - `organisers`: List of users who are event organisers.
    - `organiser_status_by_event`: Dictionary mapping event IDs to organiser
      status for the current user.

    **Template**
    - `events/event_list.html`
    """
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = "object_list"
    paginate_by = 9

    def get_queryset(self):
        # Get the base queryset filtered by current or future events
        now = timezone.now().date()
        queryset = super().get_queryset().filter(start_date__gte=now)

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
                date_start = timezone.datetime.strptime(
                    date_start, "%Y-%m-%d").date()
                queryset = queryset.filter(start_date__gte=date_start)
            except ValueError:
                messages.error(self.request, "Invalid start date format.")

        if date_end:
            try:
                date_end = timezone.datetime.strptime(
                    date_end, "%Y-%m-%d").date()
                queryset = queryset.filter(end_date__lte=date_end)
            except ValueError:
                messages.error(self.request, "Invalid end date format.")

        # Annotate and order events by their start datetime
        queryset = queryset.annotate(
            registrations_count=Count('registrations'),
            is_full=Case(
                When(registrations_count__gte=F('capacity'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            start_datetime=Concat('start_date', Value(' '), 'start_time',
                                  output_field=DateTimeField())
        ).order_by('start_datetime').distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Current date and time
        today = timezone.now().date()
        current_time = timezone.now().time()

        # Calculate whether each event is in the past
        for event in context['object_list']:
            if isinstance(event.end_date, datetime):
                event_end_date = event.end_date.date()
            else:
                event_end_date = event.end_date

            event.is_past = (
                event_end_date < today or
                (event_end_date == today and event.end_time <= current_time)
            )
            # Show event is full
            event.is_full = event.registrations_count >= event.capacity

        # Add additional context for category choices, today, and current time
        context['category_choices'] = Event.CATEGORY_CHOICES
        context['today'] = today
        context['now'] = timezone.now()

        # Registered events for the authenticated user
        if self.request.user.is_authenticated:
            registered_event_ids = Registration.objects.filter(
                user=self.request.user
            ).values_list('event__id', flat=True)
            context['registered_events'] = list(registered_event_ids)

        context['today'] = timezone.now()

        # Get a list of users who are organisers
        organisers = User.objects.filter(events__isnull=False).distinct()
        context['organisers'] = organisers

        # Organiser status for each event
        context['organiser_status_by_event'] = {
            event.id: (event.organiser == self.request.user)
            for event in context['object_list']
        }

        return context


# Event detail view
class EventDetailView(DetailView):
    """
    Displays details for a specific event.

    **Model**
    - Displays an individual instance of the `Event` model.

    **Context**
    - `event`: The event instance being displayed.
    - `form`: The `EventRegistrationForm` for event registration.
    - `is_registered`: Boolean indicating whether the user is
        registered for the event.
    - `event_has_taken_place`: Boolean indicating if
        the event has already occurred.

    **Template**
    - `events/event_detail.html`
    """
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        event_id = self.kwargs.get('pk')
        return get_object_or_404(Event, id=event_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventRegistrationForm()
        context['is_registered'] = Registration.objects.filter(
            user=self.request.user, event=self.object
        ).exists() if self.request.user.is_authenticated else False

        # Get the current date and time
        today = timezone.localtime(timezone.now())

        event_start_datetime = timezone.make_aware(
            datetime.combine(self.object.start_date, self.object.start_time)
        )

        # Check if the event has already taken place
        context['event_has_taken_place'] = event_start_datetime <= today

        # Add is_full property to the context
        registrations_count = self.object.registrations.count()
        context['event_is_full'] = registrations_count >= self.object.capacity

        # Add data to context
        context['form'] = EventRegistrationForm()
        return context


@login_required
def create_event(request):
    """
    Allows event organisers to create a new event with associated location.

    **Forms**
    - `EventForm`: Captures event details.
    - `LocationForm`: Captures location details.

    **Template**
    - `events/create_event.html`
    """
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        location_form = LocationForm(request.POST)
        if event_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            event = event_form.save(commit=False)
            event.location = location
            event.organiser = request.user
            event.save()
            return redirect('created_events')
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
    """
    Allows event organisers to edit an existing event they own.

    **Model**
    - Edits an individual instance of the `Event` model.

    **Forms**
    - `EventForm`: Captures updated event details.
    - `LocationForm`: Captures updated location details.

    **Template**
    - `events/edit_event.html`
    """
    event = get_object_or_404(Event, id=event_id)

    # Only allow the organiser to edit the event
    if request.user != event.organiser:
        messages.error(request, "You are not authorised to edit this event.")
        return redirect('event_detail', pk=event.id)

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        location_form = LocationForm(request.POST, instance=event.location)

        if event_form.is_valid() and location_form.is_valid():
            # Save the location first
            location = location_form.save()

            # Save the event
            event = event_form.save(commit=False)
            event.location = location
            event.save()

            messages.success(request, "Event updated successfully.")
            return redirect('event_detail', pk=event.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        event_form = EventForm(instance=event)
        location_form = LocationForm(instance=event.location)

    return render(request, 'events/edit_event.html', {
        'form': event_form,
        'location_form': location_form,
        'event': event,
    })


@login_required
def delete_event(request, event_id):
    """
    Allows event organisers to delete an event they own.

    **Model**
    - Deletes an individual instance of the `Event` model.

    **Template**
    - None. Redirects to `created_events`
      on success or `event_detail` otherwise.
    """
    event = get_object_or_404(Event, id=event_id, organiser=request.user)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('created_events')

    return redirect('event_detail', pk=event.id)


@login_required
def created_events_view(request):
    """
    Displays a list of events created by the logged-in organiser.

    **Model**
    - Displays data from the `Event` model.

    **Context**
    - `events`: A list of `Event` instances created by the organiser.

    **Template**
    - `events/created_events.html`
    """
    events = Event.objects.filter(organiser=request.user)
    return render(request, 'events/created_events.html', {'events': events})


# Register as event user or event organiser
def register(request):
    """
    Handles user registration, adding them to the appropriate group.

    **Forms**
    - `CustomUserCreationForm`: Captures user registration details.

    **Template**
    - `account/signup.html`
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            user_type = form.cleaned_data['user_type']

            # Get the appropriate group based on user type
            try:
                group_name = user_type.replace('_', ' ').title()
                group = Group.objects.get(name=group_name)
                user.groups.add(group)  # Add the user to the selected group
            except Group.DoesNotExist:
                messages.error(request, 'User type group does not exist.')
                return redirect('signup')

            login(request, user)  # Log in the user
            messages.success(request, 'Registration successful!'
                                      ' You are now logged in.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})


# Registration view for events
@login_required
def register_for_event(request, event_id):
    """
    Allows users to register for an event.

    **Model**
    - Registers the user for an individual instance of the `Event` model.

    **Forms**
    - `EventRegistrationForm`: Captures user email for registration.

    **Template**
    - `events/event_detail.html`
    """
    event = get_object_or_404(Event, id=event_id)

    # Prevent organisers from registering for events
    if request.user == event.organiser:
        messages.warning(request, "Organisers cannot register"
                         " for their own events.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the user is already registered for this event
            registration_exists = Registration.objects.filter(
                user=request.user, event=event
            ).exists()

            if registration_exists:
                messages.warning(
                    request, 'You are already registered for this event.'
                )
                return redirect('event_list')

            # Check if the event is full
            if event.capacity <= event.registrations.count():
                messages.warning
                (request, 'This event has reached its capacity.')
                return redirect('event_list')

            # Create a new registration
            registration = Registration(user=request.user, event=event)

            try:
                # Validate the registration
                registration.clean()  # Validation on model level
                registration.save()

                # Send confirmation email
                send_mail(
                    subject=f"Registration Confirmation for {event.title}",
                    message=(
                        f"Thank you for registering for {event.title} on "
                        f"{event.start_date} at {event.start_time}."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )

                messages.success(request, 'You have successfully registered'
                                 ' for the event! A confirmation'
                                 ' email has been sent.')
                return redirect('event_list')

            except ValidationError as e:
                messages.error(request, str(e))  # Show validation error
            except Exception as e:
                messages.error(request, 'Registration successful,'
                               ' but failed to send confirmation email.')

    else:
        form = EventRegistrationForm()

    # Check if user is already registered for the event
    is_registered = Registration.objects.filter(
        user=request.user, event=event).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'form': form,
        'is_registered': is_registered
    })


# Unregister from an event
@login_required
def unregister_from_event(request, event_id):
    """
    Allows users to unregister from an event they are registered for.

    **Model**
    - Deletes a `Registration` instance.

    **Template**
    - None. Redirects to `registered_events`.
    """
    # Get the event object
    event = get_object_or_404(Event, id=event_id)

    # Get the registration object directly, or raise a 404 if it doesn't exist
    registration = get_object_or_404(
        Registration, user=request.user, event=event)

    # Delete the registration
    registration.delete()
    messages.success(request, 'You have successfully'
                     ' unregistered from the event.')

    return redirect('registered_events')


@login_required
def registered_events(request):
    """
    Displays a list of events the user is registered for,
    categorised into upcoming and past events.

    **Model**
    - Displays data from the `Registration` model.

    **Context**
    - `upcoming_events`: List of upcoming events the user is registered for.
    - `past_events`: List of past events the user was registered for.

    **Template**
    - `events/registered_events.html`
    """
    # Get all events the user is registered for
    registered_events = Registration.objects.filter(user=request.user)

    # Get the current datetime and today's date
    current_datetime = timezone.now()
    today_date = current_datetime.date()

    # Categorize events
    past_events = registered_events.filter(
        event__end_date__lt=today_date
    )
    today_events = registered_events.filter(
        event__start_date__lte=today_date,
        event__end_date__gte=today_date
    )
    upcoming_events = registered_events.filter(
        event__start_date__gt=today_date
    )

    context = {
        'past_events': past_events,
        'today_events': today_events,
        'upcoming_events': upcoming_events,
    }

    return render(request, 'events/registered_events.html', context)


# organiser access to registered attendees
@login_required
def attendee_list(request, event_id):
    """
    Displays the list of attendees for an event,
    accessible only to the event organiser.

    **Model**
    - Displays data from the `Registration` model.

    **Context**
    - `event`: The event instance for which attendees are being displayed.
    - `attendees`: A list of users registered for the event.

    **Template**
    - `events/attendee_list.html`
    """
    # Get the event and ensure the user is the organizer
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organiser:
        messages.warning(
            request,
            "You are not authorised to view the attendees for this event."
        )
        return redirect('event_list')

    # Retrieve attendees registered for the event
    attendees = Registration.objects.filter(event=event).select_related('user')

    context = {
        'event': event,
        'attendees': attendees,
    }
    return render(request, 'events/attendee_list.html', context)
