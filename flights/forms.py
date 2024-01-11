from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Airport, Passenger, Flight

class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'city']

    def clean_code(self):
        code = self.cleaned_data['code']

        if not code.isalpha():
            raise forms.ValidationError("The airport code should only contain letters.")

        return code

    def clean_city(self):
        city = self.cleaned_data['city']

        if not city.isalpha():
            raise forms.ValidationError("The airport city should only contain letters.")
            
        return city

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first', 'last']

    def clean_first(self):
        first = self.cleaned_data['first']

        if not first.isalpha():
            raise forms.ValidationError("The first name should only contain letters.")

        return first

    def clean_last(self):
        last = self.cleaned_data['last']

        if not last.isalpha():
            raise forms.ValidationError("The last name should only contain letters.")
            
        return last

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['origin', 'destination', 'duration']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']