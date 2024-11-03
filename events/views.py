from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import TemplateView, DetailView
from .models import Event, Registration, Location
from .forms import EventForm, LocationForm, CombinedEventForm, CustomUserCreationForm, EventRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Value, DateTimeField
from django.db.models.functions import Concat

# Create your views here.
class EventsList(generic.ListView):
    model = Event
    template_name = 'events/event_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(start_date__gt=timezone.now().date())

        category = self.request.GET.get('category', '')
        date_start = self.request.GET.get('date_start', '')
        date_end = self.request.GET.get('date_end', '')
        price_min = self.request.GET.get('price_min', '')
        price_max = self.request.GET.get('price_max', '')
        free_only = self.request.GET.get('free', '')

        # Filter by category
        if category:
            queryset = queryset.filter(category=category)

        # Filter by price
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

        # Filter by free events
        if free_only:
            queryset = queryset.filter(free=True)

        # Filter by dates
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

        # Combine start_date and start_time for ordering
        queryset = queryset.annotate(
            start_datetime=Concat('start_date', Value(' '), 'start_time', output_field=DateTimeField())
        ).order_by('start_datetime').distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Event.CATEGORY_CHOICES

        # Get registered events for the logged-in user
        if self.request.user.is_authenticated:
            registered_event_ids = Registration.objects.filter(user=self.request.user).values_list('event__id', flat=True)
            context['registered_events'] = list(registered_event_ids)

        context['today'] = timezone.now()

        return context


class HomeView(TemplateView):
    template_name = 'home.html'


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
        return context


@login_required
def create_event(request):
    if request.method == 'POST':
        combined_form = CombinedEventForm(request.POST)

        if combined_form.is_valid():
            # Save location first
            location = Location.objects.create(
                venue_name=combined_form.cleaned_data['venue_name'],
                address_line_1=combined_form.cleaned_data['address_line_1'],
                address_line_2=combined_form.cleaned_data['address_line_2'],
                town_city=combined_form.cleaned_data['town_city'],
                county=combined_form.cleaned_data['county'],
                postcode=combined_form.cleaned_data['postcode']
            )

            # Create event with the saved location
            event = Event.objects.create(
                title=combined_form.cleaned_data['title'],
                category=combined_form.cleaned_data['category'],
                start_date=combined_form.cleaned_data['start_date'],
                start_time=combined_form.cleaned_data['start_time'],
                end_date=combined_form.cleaned_data['end_date'],
                end_time=combined_form.cleaned_data['end_time'],
                description=combined_form.cleaned_data['description'],
                capacity=combined_form.cleaned_data['capacity'],
                price=combined_form.cleaned_data['price'],
                free=combined_form.cleaned_data['free'],
                organiser=request.user,
                location=location
            )

            messages.success(request, 'Event created successfully!')
            return redirect('Event_List')  # Redirect to the event list page
        else:
            messages.error(request, 'Please correct the errors below.')

            # Print combined form errors for debugging
            print("Combined Form Errors:", combined_form.errors)

    else:
        combined_form = CombinedEventForm()

    return render(request, 'events/create_event.html', {
        'combined_form': combined_form
    })


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


# Registration view for events
@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the user is already registered for this event
            if Registration.objects.filter(user=request.user, event=event).exists():
                messages.warning(request, 'You are already registered for this event.')
                return redirect('Event_List')

            # Check if the event is full
            if event.capacity <= event.registrations.count():
                messages.warning(request, 'This event has reached its capacity.')
                return redirect('Event_List')

            # Create a new registration
            registration = Registration(user=request.user, event=event)

            try:
                # Validate the registration (this will raise a ValidationError if invalid)
                registration.clean()  
                registration.save()  # Save the registration

                # Send confirmation email
                send_mail(
                    subject=f"Registration Confirmation for {event.title}",
                    message=f"Thank you for registering for {event.title} on {event.start_date} at {event.start_time}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                messages.success(request, 'You have successfully registered for the event! A confirmation email has been sent.')
            except ValidationError as e:
                messages.error(request, str(e))  # Show validation error
            except Exception as e:
                messages.error(request, 'Registration successful, but failed to send confirmation email.')

            return redirect('Event_List')
    else:
        form = EventRegistrationForm()

    is_registered = Registration.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/event_detail.html', {'event': event, 'form': form, 'is_registered': is_registered})


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

    # Get current date and time
    now = timezone.now()

    # Separate into upcoming and past events
    upcoming_events = [registration for registration in registered_events if registration.event.start_date >= now.date()]
    past_events = [registration for registration in registered_events if registration.event.start_date < now.date()]

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    return render(request, 'events/registered_events.html', context)