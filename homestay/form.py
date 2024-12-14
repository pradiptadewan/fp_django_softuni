from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, UserProfile, Room, Review, Homestay, Facility


# Form Registrasi Pengguna
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Form untuk Mengedit Profil Pengguna
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']  # Daftar field yang ingin diupdate

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Ambil user dari parameter
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user  # Set user yang sedang login jika ada


# Form Pemesanan Kamar
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out', 'status']  # Hapus 'user'

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if not check_in or not check_out:
            raise forms.ValidationError("Both check-in and check-out dates are required.")

        if check_out <= check_in:
            raise forms.ValidationError("Check-out date must be after the check-in date.")

        return cleaned_data

# Form Review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    def __init__(self, *args, **kwargs):
        homestay_id = kwargs.pop('homestay_id', None)
        super().__init__(*args, **kwargs)
        self.fields['homestay'] = forms.IntegerField(
            widget=forms.HiddenInput(),
            initial=homestay_id
        )


# Form untuk Mengedit Room
class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'price', 'availability', 'image']

# Membuat Homestay
class HomestayForm(forms.ModelForm):
    facilities = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',  # Tambahkan class Bootstrap
        }),
        required=False
    )


    class Meta:
        model = Homestay
        fields = ['name', 'slug', 'description', 'address', 'phone', 'email', 'image', 'facilities', 'price']

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Homestay.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Slug already exists. Please choose a different one.")
        return slug

    def clean_facilities(self):
        facilities = self.cleaned_data.get('facilities')
        if not facilities:
            raise forms.ValidationError("Please select at least one facility.")
        return facilities

#Membuat Kamar
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'price', 'image', 'number_of_guests', 'availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['availability'].initial = True