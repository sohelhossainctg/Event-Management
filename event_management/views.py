from django.shortcuts import render
from events.models import Event
from bookings.models import Booking
from django.db.models import Q
from datetime import datetime


def home(request):
    query = request.GET.get('q')
    filters = Q()

    if query:
        try:
            event_date = datetime.strptime(query, "%d-%m-%Y").date()
            # যদি successful হয় তাহলে তারিখ দিয়ে ফিল্টার করা 
            filters &= Q(date=event_date)
        except ValueError:
            # যদি তারিখ না হয় তাহলে event name ও location দিয়ে ফিল্টার করা
            filters &= Q(event_name__icontains=query) | Q(location__icontains=query)


    data = Event.objects.filter(filters).distinct()
    total_events = data.count()

    # Check if the user is logged in to handle booking status
    if request.user.is_authenticated:
        for event in data:
            # প্রত্যেক ইভেন্টে `has_booked` attribute এড করা হয়েছে যারা লগইন করেছে তাদের জন্য
            event.has_booked = Booking.objects.filter(event=event, user=request.user).exists()
    else:
        for event in data:
            event.has_booked = False # যারা লগইন করে নাই তাদের জন্য has_booked False করা হয়েছে। 

    context = {
        "data": data,
        "total_events": total_events,
    }

    return render(request, 'home.html', context=context)


