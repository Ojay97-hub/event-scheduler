# Library imports
from datetime import datetime

# Third-party imports
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# Location model for creating an event
class Location(models.Model):
    """
    Represents a location where an event will take place.

    **Fields**
    - `venue_name` (CharField): Name of the venue.
    - `address_line_1` (CharField): Primary address of the location.
    - `address_line_2` (CharField, optional): Secondary address line.
    - `town_city` (CharField): Town or city where the location is situated.
    - `county` (CharField, optional): County or region of the location.
    - `postcode` (CharField): Postal code of the location.
    - `is_online` (BooleanField): Indicates if the event is online.

    **Methods**
    - `current_event_title`: Returns the title of the next upcoming event 
       at this location or "No Upcoming Event".
    - `get_events`: Retrieves all events related to this location.

    **Relationships**
    - Related to `Event` via a `ForeignKey` with the `related_name='events'`.
    """
    venue_name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=300)
    address_line_2 = models.CharField(max_length=300, blank=True, null=True)
    town_city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20)
    is_online = models.BooleanField(default=False)

    def current_event_title(self):
        event = self.events.filter(start_date__gte=timezone.now()).first()
        return event.title if event else "No Upcoming Event"

    def get_events(self):
        return self.events.all()  # Retrieve all events related to this location

    def __str__(self):
        return f"{self.venue_name}, {self.town_city}, {self.postcode}"

    
# Event model
class Event(models.Model):
    """
    Represents an event organised by a user.

    **Fields**
    - `id` (AutoField): Primary key for the event.
    - `title` (CharField): Title of the event.
    - `image_url` (URLField): URL to the event's image.
    - `start_date` (DateTimeField): Date and time when the event starts.
    - `end_date` (DateTimeField): Date and time when the event ends.
    - `start_time` (TimeField): Start time of the event.
    - `end_time` (TimeField): End time of the event.
    - `description` (TextField): Description of the event.
    - `capacity` (PositiveIntegerField): Maximum number of attendees.
    - `category` (CharField): Event category chosen from predefined choices.
    - `price` (DecimalField, optional): Price for the event tickets.
    - `free` (BooleanField): Indicates whether the event is free.
    - `canceled` (BooleanField): Indicates if the event is canceled.

    **Methods**
    - `save`: Overrides save to automatically set `free` based on `price`
        and default `end_date`/`end_time` values.
    - `get_status`: Returns the status of the event
        ('Upcoming', 'Past', or 'Canceled').
    - `capacity_status`: Returns a string indicating available
       spots or if the event is full.

    **Relationships**
    - Related to `Location` via a `ForeignKey` with `related_name='events'`.
    - Related to `User` (organiser) via a `ForeignKey`
      with `related_name='events'`.
    """
    CATEGORY_CHOICES = [
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
        ('meetup', 'Meetup'),
        ('networking', 'Networking'),
        ('seminar', 'Seminar'),
        ('concert', 'Concert'),
        ('festival', 'Festival'),
        ('sports', 'Sports Event'),
        ('fundraiser', 'Fundraiser'),
        ('exhibition', 'Exhibition'),
        ('class', 'Class'),
        ('party', 'Party'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image_url = models.URLField(
        max_length=500, blank=False, null=False,
        default="https://example.com/default-image.jpg")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    start_time = models.TimeField(default="09:00")
    end_time = models.TimeField(default="17:00")
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='events', null=True)
    organiser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events', null=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default='workshop')
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    free = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Automatically set `free` to True if price is None or 0
        self.free = self.price is None or self.price == 0
        # Ensure start_date and end_date are timezone-aware
        if self.start_date and timezone.is_naive(self.start_date):
            self.start_date = timezone.make_aware(self.start_date)
        if self.end_date and timezone.is_naive(self.end_date):
            self.end_date = timezone.make_aware(self.end_date)

        # Set default for end time if not provided
        if not self.end_time:
            self.end_time = (datetime.combine(
                self.start_date, self.start_time) + timezone.timedelta(
                    hours=1)).time()

        super().save(*args, **kwargs)

    def get_status(self):
        if self.canceled:
            return 'Canceled'
        start_datetime = timezone.make_aware(datetime.combine(
            self.start_date, self.start_time))
        if start_datetime < timezone.now():
            return 'Past'
        return 'Upcoming'

    def capacity_status(self):
        remaining_spots = self.capacity - self.registrations.count()
        if remaining_spots <= 0:
            return "Event Full"
        return f"{remaining_spots} spots remaining"

    def __str__(self):
        return self.title

# Registering for events 
class Registration(models.Model):
    """
    Represents a user's registration for an event.

    **Fields**
    - `user` (ForeignKey): The user who registered.
    - `event` (ForeignKey): The event for which the user registered.
    - `registered_at` (DateTimeField): Timestamp when the user registered.

    **Methods**
    - `clean`: Ensures the user cannot register for past events or full events.

    **Relationships**
    - Related to `User` and `Event` via `ForeignKey`.

    **String Representation**
    - Returns a string indicating the user and event registered for.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.event.get_status() == 'Past':
            raise ValidationError("Cannot register for a past event.")
        if self.event.capacity_status() == "Event Full":
            raise ValidationError("Cannot register, event is full.")

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"