# Seeds demo events (2026-2029) so the live portfolio site always has
# upcoming events to browse.

from datetime import datetime, time, timezone as dt_timezone
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


DEMO_USERNAME = 'eventory_team'

IMG = 'https://images.unsplash.com/photo-{}?w=800&q=80'

LOCATIONS = {
    'online': dict(
        venue_name='Online (Zoom)', address_line_1='Online',
        town_city='Online', postcode='N/A', is_online=True),
    'london': dict(
        venue_name='The Hackney Exchange', address_line_1='12 Mare Street',
        town_city='London', county='Greater London', postcode='E8 4RP'),
    'manchester': dict(
        venue_name='Northern Quarter Hall', address_line_1='45 Oldham Street',
        town_city='Manchester', county='Greater Manchester',
        postcode='M1 1JG'),
    'bristol': dict(
        venue_name='Harbourside Pavilion', address_line_1='1 Canons Road',
        town_city='Bristol', postcode='BS1 5TX'),
    'cardiff': dict(
        venue_name='Bute Park Lawns', address_line_1='North Road',
        town_city='Cardiff', county='South Glamorgan', postcode='CF10 3ER'),
    'edinburgh': dict(
        venue_name='Old Town Studios', address_line_1='8 Cowgate',
        town_city='Edinburgh', postcode='EH1 1JR'),
}

# (title, category, location, start, end, start_time, end_time,
#  capacity, price, image id, description)
EVENTS = [
    ('Intro to Django: Build Your First Web App', 'workshop', 'online',
     (2026, 11, 18), (2026, 11, 18), time(18, 0), time(20, 30), 40, None,
     '1517048676732-d65bc937f952',
     'A hands-on evening workshop for beginners. Set up a Django project, '
     'build models, views and templates, and deploy a simple app by the '
     'end of the session.'),
    ('Winter Tech Networking Night', 'networking', 'london',
     (2026, 12, 3), (2026, 12, 3), time(18, 30), time(21, 30), 120,
     Decimal('10.00'), '1556761175-b413da4baf72',
     'Meet developers, designers and founders over drinks and canapés. '
     'Bring business cards and a 30-second intro.'),
    ('UX Design Systems Webinar', 'webinar', 'online',
     (2027, 1, 20), (2027, 1, 20), time(12, 0), time(13, 0), 300, None,
     '1522202176988-66273c2fd55f',
     'How product teams build, document and scale a design system. '
     'Includes a live Q&A with practising designers.'),
    ('Spring Charity 10K Run', 'sports', 'cardiff',
     (2027, 4, 11), (2027, 4, 11), time(9, 0), time(13, 0), 500,
     Decimal('15.00'), '1461896836934-ffe607ba8211',
     'A scenic 10K loop through Bute Park. All entry fees go to local '
     'youth sports clubs. Medals for every finisher.'),
    ('Full-Stack Developer Conference 2027', 'conference', 'manchester',
     (2027, 6, 15), (2027, 6, 16), time(9, 0), time(17, 30), 400,
     Decimal('149.00'), '1540575467063-178a50c2df87',
     'Two days of talks on Python, JavaScript, cloud deployment and '
     'accessibility, with hands-on breakout sessions.'),
    ('Summer Sounds Festival', 'festival', 'bristol',
     (2027, 8, 21), (2027, 8, 22), time(12, 0), time(23, 0), 2000,
     Decimal('65.00'), '1533174072545-7a4b6ad7a6c3',
     'A weekend of live music, street food and craft stalls on the '
     'harbourside, featuring local and touring acts.'),
    ('Watercolour Painting for Beginners', 'class', 'edinburgh',
     (2027, 10, 9), (2027, 10, 9), time(10, 0), time(14, 0), 15,
     Decimal('35.00'), '1513475382585-d06e58bcb0e0',
     'A relaxed class covering brushes, washes and colour mixing. '
     'All materials are provided. No experience needed.'),
    ('Open Source Contributors Meetup', 'meetup', 'london',
     (2028, 2, 16), (2028, 2, 16), time(18, 30), time(21, 0), 60, None,
     '1515187029135-18ee286d815b',
     'Pair up and make your first open source contribution. Maintainers '
     'will be on hand with good-first-issues ready to go.'),
    ('Live Jazz & Soul Night', 'concert', 'manchester',
     (2028, 5, 20), (2028, 5, 20), time(19, 30), time(23, 0), 250,
     Decimal('22.50'), '1501281668745-f7f57925c3b4',
     'An evening of jazz standards and soul classics from a six-piece '
     'band. Doors open at 7pm.'),
    ('Digital Art Exhibition: Pixels & Paint', 'exhibition', 'bristol',
     (2028, 9, 1), (2028, 9, 14), time(10, 0), time(18, 0), 1000, None,
     '1544531586-fde5298cdd40',
     'A two-week exhibition showcasing digital and mixed-media works '
     'from emerging artists across the UK.'),
    ('AI for Small Business Seminar', 'seminar', 'online',
     (2029, 3, 14), (2029, 3, 14), time(14, 0), time(16, 0), 200, None,
     '1475721027785-f74eccf877e2',
     'Practical ways small businesses can use AI tools for marketing, '
     'customer support and admin, without the jargon.'),
    ('New Year Community Fundraiser Party', 'party', 'cardiff',
     (2029, 12, 31), (2029, 12, 31), time(20, 0), time(23, 59), 300,
     Decimal('25.00'), '1530103862676-de8c9debad1d',
     'See in the new year with music, food and a raffle. All proceeds '
     'support the local food bank.'),
]


def _aware(ymd):
    return datetime(*ymd, 12, 0, tzinfo=dt_timezone.utc)


def seed_events(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Location = apps.get_model('events', 'Location')
    Event = apps.get_model('events', 'Event')

    organiser, _ = User.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={'password': make_password(None),
                  'first_name': 'Eventory', 'last_name': 'Team'},
    )

    for (title, category, loc_key, start, end, start_time, end_time,
         capacity, price, image_id, description) in EVENTS:
        if Event.objects.filter(title=title, organiser=organiser).exists():
            continue
        location = Location.objects.create(**LOCATIONS[loc_key])
        Event.objects.create(
            title=title,
            category=category,
            location=location,
            organiser=organiser,
            start_date=_aware(start),
            end_date=_aware(end),
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            price=price,
            # Historical models skip Event.save(), so set `free` here
            free=price is None,
            image_url=IMG.format(image_id),
            description=description,
        )


def remove_events(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    Location = apps.get_model('events', 'Location')
    Event = apps.get_model('events', 'Event')

    events = Event.objects.filter(organiser__username=DEMO_USERNAME)
    location_ids = list(events.values_list('location_id', flat=True))
    events.delete()
    Location.objects.filter(id__in=location_ids).delete()
    User.objects.filter(username=DEMO_USERNAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0006_location_is_online_alter_event_image_url'),
    ]

    operations = [
        migrations.RunPython(seed_events, remove_events),
    ]
