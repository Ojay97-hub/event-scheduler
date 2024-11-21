# Third-party imports
from django.contrib import admin
from django.utils import timezone
from django_summernote.admin import SummernoteModelAdmin

# Local imports
from .models import Event, Registration, Location

class RegistrationInline(admin.TabularInline):
    """
    Inline admin for managing `Registration` objects within the `Event` admin panel.

    **Model**
    - `Registration`: Allows managing registrations directly from the event admin interface.

    **Attributes**
    - `model`: Specifies the `Registration` model.
    - `extra`: Number of empty forms displayed for adding new registrations (default is 1).
    """
    model = Registration
    extra = 1

class StatusFilter(admin.SimpleListFilter):
    """
    Custom admin filter for filtering events based on their status (upcoming or past).

    **Attributes**
    - `title`: Display name of the filter in the admin interface.
    - `parameter_name`: The query parameter used for filtering.

    **Methods**
    - `lookups`: Returns the filter options ('upcoming' and 'past').
    - `queryset`: Filters the queryset based on the selected status.
    """
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns the lookup options for the filter.
        """
        return (
            ('upcoming', 'Upcoming'),
            ('past', 'Past'),
        )

    def queryset(self, request, queryset):
        """
        Filters the queryset based on the selected status.

        **Returns**
        - `upcoming`: Events starting on or after the current date/time.
        - `past`: Events that have already occurred.
        """
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gte=timezone.now())
        if self.value() == 'past':
            return queryset.filter(start_date__lt=timezone.now())
        return queryset

class EventsAdmin(SummernoteModelAdmin):
    """
    Custom admin interface for managing `Event` objects.

    **Model**
    - `Event`: Represents events created by organisers.

    **Attributes**
    - `list_display`: Fields displayed in the event list in the admin panel.
    - `search_fields`: Fields that can be searched using the admin's search bar.
    - `list_filter`: Filters available in the admin panel for refining event lists.
    - `summernote_fields`: Fields that use the Summernote WYSIWYG editor (e.g., `description`).
    """
    list_display = (
        'title', 'description', 'start_date', 'start_time', 'end_date', 
        'end_time', 'location', 'capacity', 'category', 'price', 
        'free', 'get_status', 'organiser'
    )
    search_fields = ['title', 'location', 'description']
    list_filter = ('start_date', 'end_date', 'category', 'location', 'free', StatusFilter)
    summernote_fields = ('description',)

class LocationAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing `Location` objects.

    **Model**
    - `Location`: Represents event locations.

    **Attributes**
    - `list_display`: Fields displayed in the location list in the admin panel.
    """
    list_display = ('venue_name', 'town_city', 'postcode', 'current_event_title')

# Register your models here
admin.site.register(Event, EventsAdmin)
admin.site.register(Registration)
admin.site.register(Location, LocationAdmin)
