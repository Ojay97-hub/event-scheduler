# Third-party imports
from django.contrib.auth.models import Group


def user_roles(request):
    """
    Adds user role information to the context for template rendering.

    **Parameters**
    - `request` (HttpRequest): The current HTTP request object.

    **Functionality**
    - Checks if the authenticated user belongs to the "Event User" or
      "Event Organiser" groups.
    - Determines the user's role based on their group membership.

    **Returns**
    - A dictionary with the following keys:
        - `is_event_user` (bool): True if the user belongs to the
          "Event User" group; otherwise, False.
        - `is_event_organiser` (bool): True if the user belongs to the
          "Event Organiser" group; otherwise, False.

    **Usage**
    - Typically used as a context processor to make user role information
      globally available in templates.

    **Example**
    - If the authenticated user is in the "Event Organiser" group:
        - `is_event_user`: False
        - `is_event_organiser`: True
    """
    if request.user.is_authenticated:
        is_event_user = request.user.groups.filter(
            name='Event User'
        ).exists()
        is_event_organiser = request.user.groups.filter(
            name='Event Organiser'
        ).exists()
    else:
        is_event_user = False
        is_event_organiser = False

    return {
        'is_event_user': is_event_user,
        'is_event_organiser': is_event_organiser,
    }
    