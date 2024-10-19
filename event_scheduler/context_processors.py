from django.contrib.auth.models import Group

def user_roles(request):
    is_event_user = request.user.groups.filter(name='Event User').exists() if request.user.is_authenticated else False
    is_event_organiser = request.user.groups.filter(name='Event Organiser').exists() if request.user.is_authenticated else False
    return {
        'is_event_user': is_event_user,
        'is_event_organiser': is_event_organiser,
    }