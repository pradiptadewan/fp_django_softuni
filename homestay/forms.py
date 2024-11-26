from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, Booking, Review  # Pastikan Anda telah mengimpor model yang benar

# Form untuk registrasi pengguna
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form untuk pemesanan kamar
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

# Form untuk ulasan
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')

        # Validasi rating agar hanya antara 1 dan 5
        if rating and not (1 <= rating <= 5):
            raise forms.ValidationError("Rating harus antara 1 hingga 5.")

        return cleaned_data
