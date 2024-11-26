from django import forms
from .models import Room, Booking, Review  # Pastikan Anda telah mengimpor model yang benar

class BookingForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.Select)

    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out', 'number_of_guests']

    def clean(self):
        cleaned_data = super().clean()
        arrival_date = cleaned_data.get('check_in')
        departure_date = cleaned_data.get('check_out')

        if arrival_date and departure_date and arrival_date >= departure_date:
            raise forms.ValidationError("Tanggal kedatangan harus sebelum tanggal keberangkatan.")

        return cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']