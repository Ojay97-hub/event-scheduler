# Third-party imports
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging

# Local imports
from .models import Event


@receiver(pre_delete, sender=Event)
def notify_attendees_and_organiser_event_deletion(sender, instance, **kwargs):
    """
    Sends email notifications to attendees and the organiser when an event
    is deleted.

    **Triggered by**
    - The `pre_delete` signal for the `Event` model.

    **Parameters**
    - `sender` (Model): The model class that sent the signal (in this case,
      `Event`).
    - `instance` (Event): The instance of the event being deleted.
    - `kwargs` (dict): Additional arguments passed to the signal.

    **Functionality**
    - Retrieves all registered attendees for the event.
    - Sends a cancellation email to each attendee.
    - Sends a confirmation email to the organiser about the cancellation.

    **Notifications**
    - **Attendees**:
      - Email includes the event title, date, and a regret message.
    - **Organiser**:
      - Email confirms the event's cancellation with details.

    **Error Handling**
    - Logs errors encountered while sending emails without interrupting the
      deletion process.
    - Logs warnings if no organiser exists for the event.

    **Logging**
    - Uses `INFO` level for successful email notifications.
    - Uses `ERROR` level for email sending failures.
    - Uses `WARNING` level if no organiser is associated with the event.
    """
    # Get the logger instance
    logger = logging.getLogger(__name__)

    registrations = instance.registrations.all()
    event_date = instance.start_date
    event_title = instance.title

    # Notify attendees
    for registration in registrations:
        attendee_email = registration.user.email
        username = registration.user.username

        try:
            send_mail(
                subject=f"Event Cancellation: {event_title}",
                message=(
                    f"Dear {username},\n\n"
                    f"We regret to inform you the event '{event_title}',\n"
                    f"scheduled on {event_date}, has been cancelled.\n\n"
                    "We apologise for any inconvenience.\n\n"
                    "Thank you,\nEventory Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[attendee_email],
                fail_silently=False,
            )
            logger.info(
                f"Email sent to attendee: {attendee_email} "
                f"for event: {event_title}"
            )
        except Exception as e:
            logger.error(
                f"Error sending email to attendee {attendee_email}: {e}"
            )

    # Notify organiser
    if instance.organiser:
        organiser_email = instance.organiser.email
        organiser_username = instance.organiser.username

        try:
            send_mail(
                subject=f"Your Event Has Been Cancelled: {event_title}",
                message=(
                    f"Dear {organiser_username},\n\n"
                    f"We would like to inform you that your event "
                    f"'{event_title}', scheduled on {event_date},\n"
                    "has been successfully cancelled.\n\n"
                    "We apologise for any inconvenience.\n\n"
                    "Thank you,\nEventory Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[organiser_email],
                fail_silently=False,
            )
            logger.info(
                f"Email sent to organiser: {organiser_email} "
                f"for event: {event_title}"
            )
        except Exception as e:
            logger.error(
                f"Error sending email to organiser {organiser_email}: {e}"
            )
    else:
        logger.warning(
            f"No organiser found for the event: {event_title}"
        )
