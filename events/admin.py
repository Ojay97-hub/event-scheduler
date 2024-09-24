from django.contrib import admin
from .models import Event
from django_summernote.admin import SummernoteModelAdmin

class EventsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'description','date', 'time', 'location', 'capacity')
    search_fields = ['title', 'location', 'description']
    list_filter = ('date', 'location')
    summernote_fields = ('description',)

# Register your models here.
admin.site.register(Event, EventsAdmin)