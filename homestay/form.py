from django import forms
from .models import Room, Booking, CustomUser # Pastikan CustomUser adalah nama model pengguna Anda

class BookingForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.Select)

    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password tidak cocok")

        return cleaned_data