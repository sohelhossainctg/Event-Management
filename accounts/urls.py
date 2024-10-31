from django.urls import path
from . views import login_view, home, logout_view, register, profile, update_profile

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
]
