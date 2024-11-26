from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking, Room, Homestay, Review
from .forms import BookingForm, RegisterForm, ReviewForm

# Home Page
def home(request):
    return render(request, 'homestay/home.html')

# About Page
def about(request):
    return render(request, 'homestay/about.html')

# Room List View (CBV)
class RoomListView(ListView):
    model = Room
    template_name = 'homestay/rooms.html'
    context_object_name = 'rooms'

# Room Detail View (CBV)
class RoomDetailView(DetailView):
    model = Room
    template_name = 'homestay/room_detail.html'
    context_object_name = 'room'

# Contact Page
def contact(request):
    return render(request, 'homestay/contact.html')

# Register User
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'homestay/register.html', {'form': form})

# Login User
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'homestay/login.html', {'form': form})

# Logout User
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

# Profile Page
@login_required
def profile(request):
    return render(request, 'homestay/profile.html')

# Booking Create View
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'homestay/booking_form.html'

    def form_valid(self, form):
        room = Room.objects.get(pk=self.kwargs['pk'])
        if room.is_available:
            form.instance.room = room
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            form.add_error(None, 'This room is not available.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('booking_confirm')

# Booking Confirmation
def booking_confirm(request):
    return render(request, 'homestay/booking_confirm.html')

# User Bookings List View
class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'homestay/bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Homestay List View
class HomestayListView(ListView):
    model = Homestay
    template_name = 'homestay/homestays.html'
    context_object_name = 'homestays'

# Homestay Detail View
class HomestayDetailView(DetailView):
    model = Homestay
    template_name = 'homestay/homestay_detail.html'
    context_object_name = 'homestay'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homestay = self.get_object()
        context['rooms'] = Room.objects.filter(homestay=homestay).order_by('room_number')
        context['reviews'] = Review.objects.filter(homestay=homestay).order_by('-created_at')
        return context

# Add Review View
class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'homestay/add_review.html'

    def form_valid(self, form):
        homestay = Homestay.objects.get(pk=self.kwargs['pk'])
        form.instance.homestay = homestay
        form.instance.user = self.request.user
        messages.success(self.request, 'Your review has been posted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homestay_detail', kwargs={'pk': self.kwargs['pk']})
