from django.urls import path
from . import views

urlpatterns = [
    path('add_event/', views.add_event, name='add_event'), 
    path('edit_event/', views.home, name='edit_event'), 
    path('update_event/<int:id>/', views.update_event, name='update_event'), 
    path('delete_event/<int:id>/', views.delete_event, name='delete_event'), 
    path('view_event/<int:id>/', views.view_event, name='view_event'), 
    path('delete_event/<int:id>/', views.delete_event, name='delete_event'),
]







