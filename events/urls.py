from . import views 
from django.urls import path
from .views import HomeView, EventsList, create_event, register, register_for_event, EventDetailView, registered_events, delete_event, edit_event, attendee_list, organiser_events

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Homepage
    path('create/', create_event, name='create_event'),  # Create event
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'), # edit event
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'), # cancel event
    path('created-events/', views.created_events_view, name='created_events'), # Created events 
    path('events/', EventsList.as_view(), name='event_list'),  # Events List
    path('events/<int:event_id>/attendees/', views.attendee_list, name='attendee_list'), # Registered attendees list
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),  # Event detail
    path('organiser/<int:organiser_id>/events/', views.organiser_events, name='organiser_events'), # view organisers page
    path('register/', register, name='register'),  # Register
    path('event/register/<int:event_id>/', register_for_event, name='event_register'),  # Event registration
    path('my-events/', registered_events, name='registered_events'),  # View for registered events
    path('unregister/<int:event_id>/', views.unregister_from_event, name='unregister_from_event'), # Unregister an event
]
