from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from rental_app.models import *

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]

class SigninForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-1 py-1 border rounded bg-white"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"w-full px-1 py-1 border rounded bg-white"}))



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User_profile
        exclude = ["user", "is_license_verified", "created_at", "updated_at"]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "pickup_location",
            "pickup_date",
            "return_date",
            "notes",
        ]

        widgets = {
            "pickup_location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Pickup Location"
            }),
            "pickup_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "return_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        pickup = cleaned_data.get("pickup_date")
        return_date = cleaned_data.get("return_date")

        if pickup and return_date and return_date < pickup:
            raise forms.ValidationError(
                "Return date must be after pickup date."
            )

        return cleaned_data
    



class ReturnBookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "actual_return_date",
            "notes"
        ]

        widgets = {

            "actual_return_date": forms.DateInput(
                attrs={"type": "date","class":"form-control"}
            ),

            "notes": forms.Textarea(
                attrs={"class":"form-control","rows":3}
            )

        }


 