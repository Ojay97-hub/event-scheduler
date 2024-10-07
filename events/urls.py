from . import views 
from django.urls import path
from .views import HomeView, EventsList, create_event, register, register_for_event 

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Homepage
    path('create/', create_event, name='create_event'),  # Create event
    path('events/', EventsList.as_view(), name='Event_Page'),  # Events page
    path('register/', register, name='register'),  # Register
    path('event/register/<int:event_id>/', register_for_event, name='event_register'),  # Event registration
]
