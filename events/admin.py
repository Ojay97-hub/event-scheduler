from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Event, Registration, Location
from django_summernote.admin import SummernoteModelAdmin

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_groups')
    
    # Method to get the list of groups a user belongs to
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'
    
    # Enable filtering and searching by groups
    list_filter = ('groups',)  
    search_fields = ('username', 'email', 'first_name', 'last_name', 'groups__name') 

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 1 

class StatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('upcoming', 'Upcoming'),
            ('past', 'Past'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gte=timezone.now())
        if self.value() == 'past':
            return queryset.filter(start_date__lt=timezone.now())
        return queryset

class EventsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'description', 'start_date', 'start_time', 'end_date', 
        'end_time', 'location', 'capacity', 'category', 'price', 
        'free', 'get_status', 'organiser')
    search_fields = ['title', 'location', 'description']
    list_filter = ('start_date', 'end_date', 'category', 'location', 'free', StatusFilter)
    summernote_fields = ('description',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'town_city', 'postcode', 'current_event_title')

# Register your models here.
admin.site.unregister(User)  # Unregister the default UserAdmin
admin.site.register(User, UserAdmin)  # Register the custom UserAdmin
admin.site.register(Event, EventsAdmin)
admin.site.register(Registration)
admin.site.register(Location, LocationAdmin)