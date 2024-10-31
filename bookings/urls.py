from django.urls import path
from . import views

urlpatterns = [
    path('book_event/<int:event_id>/', views.book_event, name='book_event'),
    path('booked_events/', views.booked_events, name='booked_events'),
]