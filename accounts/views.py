from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserUpdateForm

# Create your views here.
def login_view(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    form = LoginForm(request.POST, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      if user is None:
        return redirect('login')
      login(request, user)
      return redirect('homepage')
    
  form = LoginForm()
  return render(request, 'accounts/login.html', {'form': form})


@login_required
def home(request):
  return render(request, 'accounts/home.html')


@login_required
def logout_view(request):
  logout(request)
  return redirect('login')



def register(request):
  if request.user.is_authenticated:
    return redirect('home')
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
  else:
    form = RegisterForm()
  return render(request, 'accounts/register.html', {'form': form})




@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'data': request.user})

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')  
    else:
        user_form = UserUpdateForm(instance=user)

    return render(request, 'accounts/update_profile.html', {'form': user_form})