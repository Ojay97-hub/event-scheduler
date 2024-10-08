from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Event(models.Model):
    """
    An event with details such as its title, date, time, location, description, capacity,
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
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='eventtype')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) 
    free = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Free events == no price
        if self.free:
            self.price = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Registration(models.Model):
    """
    A model representing the registration of a user for a specific event.

    Attributes:
        user (ForeignKey): A reference to the User who registered for the event.
        event (ForeignKey): A reference to the Event for which the user is registered.
        registered_at (DateTimeField): The date and time when the user registered for the event. 
                                       This field is automatically set to the current date and time
                                       when a registration instance is created.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"
