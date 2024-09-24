from . import views
from django.urls import path

urlpatterns = [
    path('', views.EventsList.as_view(), name='Event_Page'),
]