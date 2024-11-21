from django.apps import AppConfig


class EventsConfig(AppConfig):
    """
    Configuration class for the 'events' app.

    **Attributes**
    - `default_auto_field` (str): Specifies the default type of primary key field for models.
    - `name` (str): The name of the app ('events').

    **Methods**
    - `ready`: Called when the app is fully loaded. This method imports the signals module to enable event cancellation notifications.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        """
        Imports the `signals` module for the 'events' app.

        **Purpose**
        - Ensures that signals, such as the pre-delete signal for sending event cancellation notifications, are connected when the app is ready.
        
        **Side Effects**
        - Imports `events.signals` to register signal handlers.
        """
        import events.signals  
