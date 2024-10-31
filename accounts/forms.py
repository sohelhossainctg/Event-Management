from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.db import models

class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
  
  

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), max_length=30)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}), max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Address'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            # Create or update the profile with mobile and address information
            Profile.objects.create(
                user=user,
                mobile=self.cleaned_data['mobile'],
                address=self.cleaned_data['address']
            )
        return user 

class UserUpdateForm(forms.ModelForm):
    mobile = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'address']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance.profile:
            self.fields['mobile'].initial = self.instance.profile.mobile
            self.fields['address'].initial = self.instance.profile.address

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.mobile = self.cleaned_data['mobile']
            profile.address = self.cleaned_data['address']
            profile.save()
        return user