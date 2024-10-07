from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Event(models.Model):
    """
    An event with details such as its title, date, time, location, description, capacity,
    and associated event types (tags).

    Attributes:
        id (AutoField): An auto-incremented primary key for identifying the event.
        title (CharField): The event's title, up to 200 characters long.
        date (DateField): The date the event is planned for.
        time (TimeField): The time the event starts.
        location (CharField): The venue or location of the event, up to 300 characters long.
        description (TextField): A detailed description of what the event is about.
        capacity (PositiveIntegerField): The maximum number of attendees allowed.
        tags (ManyToManyField): A many-to-many relationship with the EventType model, categorizing the event.
    """
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    description = models.TextField()
    capacity = models.PositiveIntegerField()

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
