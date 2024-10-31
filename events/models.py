from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    date = models.DateField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.PositiveIntegerField() 
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name

    @property
    def is_fully_booked(self):
        from bookings.models import Booking  
        bookings_count = Booking.objects.filter(event=self).count()
        return bookings_count >= self.capacity

