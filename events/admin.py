from django.contrib import admin
from .models import Event, Registration
from django_summernote.admin import SummernoteModelAdmin

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 1 

class EventsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'description','date', 'time', 'location', 'capacity', 'category')
    search_fields = ['title', 'location', 'description']
    list_filter = ('date', 'location')
    summernote_fields = ('description',)

# Register your models here.
admin.site.register(Event, EventsAdmin)
admin.site.register(Registration)