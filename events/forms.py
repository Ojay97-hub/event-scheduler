from django import forms
from .models import Event, Location
from django.forms.widgets import DateInput, TimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

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

# Event form for creation
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'image_url', 'start_date', 'start_time', 'end_date', 'end_time', 'description', 'capacity', 'category', 'price', 'free']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter a valid image URL'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        if start_date == end_date and start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        # Image URL validation
        image_url = cleaned_data.get('image_url')
        if image_url:
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')
            parsed_url = urlparse(image_url)
            path = parsed_url.path.lower()

            # Remove query parameters from the URL path before checking extension
            path_without_query = path.split('?')[0]

            if not path_without_query.endswith(valid_extensions):
                raise ValidationError("Please enter a URL that points to a valid image (e.g., .jpg, .png).")

        return cleaned_data

# Location form for creating a new location
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['venue_name', 'address_line_1', 'address_line_2', 'town_city', 'county', 'postcode']
        widgets = {
            'venue_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue name'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 2 (optional)'}),
            'town_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter town or city'}),
            'county': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter county (optional)'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postcode'}),
        }

# Register as event user or event organiser
class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('event_user', 'Event User'),
        ('event_organiser', 'Event Organiser'),
    )

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email address'  
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

# Event registration
class EventRegistrationForm(forms.Form):
    email = forms.EmailField(label="Enter your email for confirmation", required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))