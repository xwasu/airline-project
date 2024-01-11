from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Airport, Passenger, Flight

class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'city']

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first', 'last']

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['origin', 'destination', 'duration']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']