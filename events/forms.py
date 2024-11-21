# Library imports
from urllib.parse import urlparse
import requests

# Third-party imports
from django import forms
from django.forms.widgets import DateInput, TimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# Local imports
from .models import Event, Location

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
    """
    A form for creating or editing events.

    **Fields**
    - `title` (CharField): Title of the event.
    - `image_url` (URLField): URL for the event's image.
    - `start_date` (DateField): Event start date.
    - `start_time` (TimeField): Event start time.
    - `end_date` (DateField): Event end date.
    - `end_time` (TimeField): Event end time.
    - `description` (TextField): Detailed description of the event.
    - `capacity` (PositiveIntegerField): Maximum number of attendees.
    - `category` (CharField): Event category (chosen from predefined options).
    - `price` (DecimalField): Price for the event.
    - `free` (BooleanField): Indicates whether the event is free.

    **Validation**
    - Ensures valid date ranges (start before end).
    - Validates that free events cannot have a price.
    - Validates the `image_url` field to ensure it points to a valid image.

    **Model**
    - Linked to the `Event` model.

    **Widgets**
    - Customises input fields with placeholders and CSS classes for better UI.
    """
    class Meta:
        model = Event
        fields = ['title', 'image_url', 'start_date', 'start_time', 'end_date',
                  'end_time', 'description', 'capacity',
                  'category', 'price', 'free']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the event title',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a valid image URL',
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select the event start date',
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Select the start time',
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select the event end date',
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Select the end time',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter a detailed description for your event',
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the maximum number of attendees',
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the ticket price (if applicable)',
                'min': 0,
            }),
            'free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_image_url(self):
        """Ensure the image URL points to a valid image."""
        image_url = self.cleaned_data.get('image_url')
        if not image_url:
            raise forms.ValidationError("This field is required.")

        try:
            response = requests.head(image_url, timeout=5)
            content_type = response.headers.get('Content-Type', '').lower()
            if 'image' not in content_type:
                raise forms.ValidationError(
                    "The URL must point to a valid image.")
        except requests.RequestException:
            raise forms.ValidationError(
                "The provided URL is not reachable or invalid.")

        return image_url

    def clean(self):
        """Custom validation for date, time, price, and free fields."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        free = cleaned_data.get('free')
        price = cleaned_data.get('price')

        # Validate dates and times
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(
              "The event's end date must occur after the start date.")
        if start_date == end_date and start_time >= end_time:
            raise forms.ValidationError(
                "The event's end time must occur after the start time.")

        # Validate price and free
        if free and price:
            raise forms.ValidationError({
                'price': "If the event is free, you cannot set a price."
            })
        if not free and (price is None or price <= 0):
            raise forms.ValidationError({
                'price': "Please enter a valid price for a paid event."
            })

        return cleaned_data

# Location form for creating a new location


class LocationForm(forms.ModelForm):
    """
    A form for creating or editing locations.

    **Fields**
    - `venue_name` (CharField): Name of the venue.
    - `address_line_1` (CharField): Primary address of the location.
    - `address_line_2` (CharField): Secondary address line (optional).
    - `town_city` (CharField): Town or city where the location is situated.
    - `county` (CharField): County or region (optional).
    - `postcode` (CharField): Postal code of the location.
    - `is_online` (BooleanField): Indicates if the event is online.

    **Model**
    - Linked to the `Location` model.

    **Widgets**
    - Customizes input fields with placeholders and CSS classes for better UI.
    """
    class Meta:
        model = Location
        fields = ['venue_name', 'address_line_1',
                  'address_line_2', 'town_city', 'county',
                  'postcode', 'is_online']
        labels = {
            'is_online': 'Online Event',
        }
        widgets = {
            'venue_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder':
                    'Enter venue name'}),
            'address_line_1': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder':
                    'Enter address line 1'}),
            'address_line_2': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder':
                    'Enter address line 2 (optional)'}),
            'town_city': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder':
                    'Enter town or city'}),
            'county': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder':
                    'Enter county (optional)'}),
            'postcode': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter postcode'}),
            'is_online': forms.CheckboxInput(attrs={
                'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set required fields based on `is_online`
        if self.data.get('is_online') == 'on':
            for field in [
                    'venue_name', 'address_line_1', 'town_city', 'postcode']:
                self.fields[field].required = False
        else:
            for field in [
                    'venue_name', 'address_line_1', 'town_city', 'postcode']:
                self.fields[field].required = True

    def clean(self):
        """Validates location fields based on whether the event is online."""
        cleaned_data = super().clean()
        is_online = cleaned_data.get('is_online')

        if is_online:
            # Skip validation for location fields if the event is online
            location_fields = [
                    'venue_name', 'address_line_1', 'address_line_2',
                    'town_city', 'county', 'postcode']
            for field in location_fields:
                cleaned_data[field] = ''  # Clear the values for consistency
        else:
            # Validate location fields for in-person events
            required_fields = [
                'venue_name', 'address_line_1', 'town_city', 'postcode']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required.")

        return cleaned_data

# Register as event user or event organiser


class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for registering users as event users or organisers.

    **Fields**
    - `username` (CharField): Username for the user.
    - `email` (EmailField): Email address of the user.
    - `password1` and `password2` (CharField): Password fields.
    - `user_type` (ChoiceField): Indicates if the user
       is an 'Event User' or 'Event Organiser'.

    **Model**
    - Linked to the `User` model.
    """
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
    """
    A form for registering users for an event.

    **Fields**
    - `email` (EmailField): Email address for event registration confirmation.
    """
    email = forms.EmailField(
        label="Enter your email for confirmation", required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'Email address'}))