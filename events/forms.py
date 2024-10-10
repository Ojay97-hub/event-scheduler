from django import forms
from .models import Event
# register/sign up
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# event form for creation
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'location', 'description', 'capacity', 'category', 'price', 'free']

# register as event user or event organiser
class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('event_user', 'Event User'),
        ('event_organiser', 'Event Organiser'),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')
        email = forms.EmailField(required=True)