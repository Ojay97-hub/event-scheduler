from . import views
from django.urls import path
from .views import HomeView, EventsList

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Homepage
    path('events/', EventsList.as_view(), name='Event_Page'),  # Events page
]