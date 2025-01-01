from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Form for renting equipment (includes date, payment method, and terms acceptance)
class RentForm(forms.Form):
    equipment_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    days = forms.IntegerField(min_value=1)
    payment_method = forms.ChoiceField(choices=[('advance', 'In advance'), ('on_pickup', 'On pickup')])
    accept_terms = forms.BooleanField(required=True, label="I accept the terms and conditions")

# Custom user registration form with additional fields for name and email
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(max_length=254, required=True, label="Email Address")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
