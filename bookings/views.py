from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from events.models import Event
from .models import Booking
from django.shortcuts import render

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # সম্পূর্ণ booked কিনা চেক করার জন্য
    if event.is_fully_booked:
        messages.error(request, "This event is fully booked.")
        return redirect('view_event', id=event.id)

    # Creator তার নিজেদের তৈরি ইভেন্ট বুক করতে না পারার জন্য। 
    if event.creator == request.user:
        messages.error(request, "You cannot book your own event.")
        return redirect('view_event', id=event.id)

    # ইউজার ইভেন্ট অলরেডি বুক করছে কিনা চেক করা 
    if Booking.objects.filter(event=event, user=request.user).exists():
        messages.info(request, "You have already booked this event.")
        return redirect('view_event', id=event.id)

    # নতুন বুকিং করা 
    Booking.objects.create(event=event, user=request.user)
    messages.success(request, "Successfully booked the event!")
    return redirect('view_event', id=event.id)


#ইউজার যা যা বুক করছে তা চেক করার জন্য 
@login_required
def booked_events(request):
    user_bookings = Booking.objects.filter(user=request.user).select_related('event')
    return render(request, 'bookings/booked_events.html', {'user_bookings': user_bookings})