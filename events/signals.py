# events/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Event

@receiver(pre_delete, sender=Event)
def notify_attendees_and_organiser_on_event_deletion(sender, instance, **kwargs):
    registrations = instance.registrations.all()
    
    # Use start_date as the event date
    event_date = instance.start_date  # Corrected field

    # Notify attendees
    for registration in registrations:
        attendee_email = registration.user.email
        username = registration.user.username
        event_title = instance.title

        # Send email to attendee
        try:
            send_mail(
                subject=f"Event Cancellation: {event_title}",
                message=f"Dear {username},\n\nWe regret to inform you that the event '{event_title}', scheduled on {event_date}, has been cancelled. We apologise for any inconvenience.\n\nThank you,\nEventory Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[attendee_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to {attendee_email}: {e}")

    # Notify organiser
    if instance.organiser:  # Check if organiser exists
        organiser_email = instance.organiser.email
        organiser_username = instance.organiser.username

        # Send email to organiser
        try:
            send_mail(
                subject=f"Your Event Has Been Cancelled: {event_title}",
                message=f"Dear {organiser_username},\n\nWe would like to inform you that your event '{event_title}', scheduled on {event_date}, has been successfully cancelled. We apologise for any inconvenience.\n\nThank you,\nEventory Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[organiser_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to {organiser_email}: {e}")
    else:
        print(f"No organiser found for the event '{instance.title}'")