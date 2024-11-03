from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from datetime import datetime
from django.db.models import Count 

# Create your models here.
class Event(models.Model):
    """
    An event with details such as its title, date, time, location, description, capacity, price/free,
    and associated category.
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
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='events', null=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='eventtype')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    free = models.BooleanField(default=False)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', null=True)

    def save(self, *args, **kwargs):
        # Set default for end date and time if not provided
        if not self.end_date:
            self.end_date = self.start_date  # Default end date to start date if not set
        if not self.end_time:
            # Set default end time to one hour after start time if not set
            self.end_time = (datetime.combine(self.start_date, self.start_time) + timezone.timedelta(hours=1)).time()
        super().save(*args, **kwargs)

    def get_status(self):
        start_datetime = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
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

class Location(models.Model):
    venue_name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=300)
    address_line_2 = models.CharField(max_length=300, blank=True, null=True)
    town_city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20)

    def current_event_title(self):
        event = self.events.filter(start_date__gte=timezone.now()).first()
        return event.title if event else "No Upcoming Event"

    def __str__(self):
        return f"{self.venue_name}, {self.town_city}, {self.postcode}"

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.event.get_status() == 'Past':
            raise ValidationError("Cannot register for a past event.")
        if self.event.capacity_status() == "Event Full":
            raise ValidationError("Cannot register, event is full.")

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"
