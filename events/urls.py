from . import views 
from django.urls import path
from .views import HomeView, EventsList, create_event, register, register_for_event, EventDetailView, registered_events

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Homepage
    path('create/', create_event, name='create_event'),  # Create event
    path('events/', EventsList.as_view(), name='Event_List'),  # Events List
    path('events/<int:id>/', EventDetailView.as_view(), name='event_detail'), # event detail
    path('register/', register, name='register'),  # Register
    path('event/register/<int:event_id>/', register_for_event, name='event_register'),  # Event registration
    path('my-events/', registered_events, name='registered_events'),  # View for registered events
    path('unregister/<int:event_id>/', views.unregister_from_event, name='unregister_from_event'), # Unregister an event
]
