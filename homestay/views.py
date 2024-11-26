from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Booking, Room, Homestay, Review
from .forms import BookingForm, RegisterForm, ReviewForm

def home(request):
    return render(request, 'homestay/index.html')

def about(request):
    return render(request, 'homestay/about.html')

def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'homestay/rooms.html', {'rooms': rooms})

def room_detail(request, pk):
    room = Room.objects.get(pk=pk)
    return render(request, 'homestay/room_detail.html', {'room': room})

def contact(request):
    return render(request, 'homestay/contact.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'homestay/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'homestay/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required  # Memastikan pengguna login sebelum mengakses profile
def profile(request):
    return render(request, 'homestay/profile.html')

def booking_form(request, room_id):
    room = Room.objects.get(pk=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            return redirect('booking_confirm')
    else:
        form = BookingForm()
    return render(request, 'homestay/booking_form.html', {'form': form, 'room': room})

def booking_confirm(request):
    return render(request, 'homestay/booking_confirm.html')

@login_required  # Memastikan pengguna login untuk melihat bookings
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'homestay/bookings.html', {'bookings': bookings})

def homestays_list(request):
    homestays = Homestay.objects.all()
    return render(request, 'homestay/homestays.html', {'homestays': homestays})

def homestay_detail(request, pk):
    homestay = Homestay.objects.get(pk=pk)
    rooms = Room.objects.filter(homestay=homestay)
    reviews = Review.objects.filter(homestay=homestay).order_by('-created_at')
    return render(request, 'homestay/homestay_detail.html', {'homestay': homestay, 'rooms': rooms, 'reviews': reviews})

@login_required  # Memastikan pengguna login untuk menambahkan review
def add_review(request, homestay_id):
    homestay = Homestay.objects.get(pk=homestay_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.homestay = homestay
            review.user = request.user
            review.save()
            return redirect('homestay_detail', pk=homestay_id)
    else:
        review_form = ReviewForm()
    return render(request, 'homestay/add_review.html', {'review_form': review_form, 'homestay': homestay})