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
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={
                'placeholder': 'Enter a valid image URL',
                'class': 'form-control',
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
                'min': 1,
            }),
            'free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_image_url(self):
        """Ensure the image URL points to a valid image format."""
        image_url = self.cleaned_data.get('image_url')
        print(f"Debug: image_url provided: {image_url}")
        if not image_url:  # Check for an empty value
            raise forms.ValidationError("This field is required.")

        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')
        parsed_url = urlparse(image_url)
        path = parsed_url.path.lower()

        # Remove query parameters from the URL path before checking extension
        path_without_query = path.split('?')[0]

        if not path_without_query.endswith(valid_extensions):
            raise forms.ValidationError("Please enter a URL that points to a valid image (e.g., .jpg, .png).")
        
        return image_url

    def clean(self):
        """Custom validation for date and time fields."""
        cleaned_data = super().clean()

        # Fetch relevant fields
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        free = cleaned_data.get('free')
        price = cleaned_data.get('price')

        # Debugging Outputs
        print(f"Debug: start_date = {start_date}, end_date = {end_date}")
        print(f"Debug: start_time = {start_time}, end_time = {end_time}")
        print(f"Debug: free = {free}, price = {price}")

        # Validate dates
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        if start_date == end_date and start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        # Validate price and free fields
        if free and price:
            self.add_error('price', "Price must be empty for free events.")
            print("Debug: Error - Price provided for a free event.")
        if not free and (price is None or price <= 0):
            self.add_error('price', "Enter a valid price for non-free events.")
            print("Debug: Error - Price is required and must be greater than 0 for non-free events.")

        # Debug cleaned data before returning
        print(f"Debug: Final cleaned_data: {cleaned_data}")
        return cleaned_data

# Location form for creating a new location
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['venue_name', 'address_line_1', 'address_line_2', 'town_city', 'county', 'postcode', 'is_online']
        labels = {
            'is_online': 'Online Event',
        }
        widgets = {
            'venue_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue name'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 2 (optional)'}),
            'town_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter town or city'}),
            'county': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter county (optional)'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postcode'}),
            'is_online': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set required fields based on `is_online`
        if self.data.get('is_online') == 'on':  # Check if "Online Event" checkbox is checked
            for field in ['venue_name', 'address_line_1', 'town_city', 'postcode']:
                self.fields[field].required = False
        else:
            for field in ['venue_name', 'address_line_1', 'town_city', 'postcode']:
                self.fields[field].required = True

    def clean(self):
        cleaned_data = super().clean()
        is_online = cleaned_data.get('is_online')

        print(f"Debug: is_online value: {is_online}")
        print(f"Debug: Initial cleaned_data: {cleaned_data}")

        if is_online:
            print("Debug: Event is marked as online. Skipping location validation.")
            # Skip validation for location fields if the event is online
            location_fields = ['venue_name', 'address_line_1', 'address_line_2', 'town_city', 'county', 'postcode']
            for field in location_fields:
                cleaned_data[field] = ''  # Clear the values for consistency
        else:
            print("Debug: Event is not online. Validating location fields.")
            # Validate location fields for in-person events
            required_fields = ['venue_name', 'address_line_1', 'town_city', 'postcode']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required.")
                    print(f"Debug: Error added for field: {field}")

        print(f"Debug: Final cleaned_data: {cleaned_data}")
        return cleaned_data

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