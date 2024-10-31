from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Event
from . import forms
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse



@login_required 
def add_event(request):
    if request.method == 'POST':
        event_form = forms.EventForm(request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.creator = request.user 
            event.save()
            return redirect('homepage')
    else:
        event_form = forms.EventForm()    
    return render(request, 'add_events.html', {'form': event_form})
  

@login_required 
def update_event(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return HttpResponse("Event not found")

    # Creator বা admin কিনা তা চেক করা
    if request.user != event.creator and not request.user.is_staff:
        return HttpResponse("You do not have permission to update this event.")

    if request.method == 'POST':
        event_form = forms.EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('view_event', id=event.id)
    else:
        event_form = forms.EventForm(instance=event)
    
    return render(request, 'update_event.html', {'form': event_form})

@login_required 
def delete_event(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return HttpResponse("Event not found")

    # Creator বা admin কিনা তা চেক করা
    if request.user != event.creator and not request.user.is_staff:
        return HttpResponse("You do not have permission to delete this event.")

    event.delete()
    return redirect('edit_event')


@login_required 
def home(request):
  data = Event.objects.filter(creator=request.user)
  total_events = data.count()
  return render(request, 'edit_events.html', {'data': data, 'total_events': total_events})





def view_event(request, id):
    try:
        event = Event.objects.get(id=id)
        bookings_count = Booking.objects.filter(event=event).count()
        remaining_seats = event.capacity - bookings_count  # Calculate remaining seats
        
        return render(request, 'view_event.html', {
            'data': event,
            'remaining_seats': remaining_seats
        })
    except Event.DoesNotExist:
        return HttpResponse("<h1>Event not found</h1>")



def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def delete_event(request, id): 
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect(reverse('homepage'))





