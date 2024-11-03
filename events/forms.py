from django import forms
from .models import Event, Location
from django.forms.widgets import DateInput, TimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['title', 'start_date', 'start_time', 'end_date', 'end_time', 'description', 'capacity', 'category', 'price', 'free']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
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

# Combined form for creating an event with location
class CombinedEventForm(forms.Form):
    # Fields from EventForm
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}))
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    start_time = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_time = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Description'}))
    capacity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}))
    free = forms.BooleanField(required=False)

    # Fields from LocationForm
    venue_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue name'}))
    address_line_1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 1'}))
    address_line_2 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address line 2 (optional)'}))
    town_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter town or city'}))
    county = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter county (optional)'}))
    postcode = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postcode'}))

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

# Register as event user or event organiser
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

# Event registration
class EventRegistrationForm(forms.Form):
    email = forms.EmailField(label="Enter your email for confirmation", required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
