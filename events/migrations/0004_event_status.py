# Generated by Django 3.2.25 on 2024-10-29 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('upcoming', 'Upcoming'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='upcoming', max_length=20),
        ),
    ]
