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