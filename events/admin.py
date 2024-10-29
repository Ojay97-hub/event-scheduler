from django.contrib import admin
from django.utils import timezone
from .models import Event, Registration
from django_summernote.admin import SummernoteModelAdmin

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

    list_display = ('title', 'description', 'date', 'time', 'start_date', 'location', 
                    'capacity', 'category', 'price', 'free', 'get_status')
    search_fields = ['title', 'location', 'description']
    list_filter = ('date','category', 'location', StatusFilter)
    summernote_fields = ('description',)

# Register your models here.
admin.site.register(Event, EventsAdmin)
admin.site.register(Registration)