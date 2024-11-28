from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking, Room, Homestay, Review, UserProfile
from .form import BookingForm, RegisterForm, ReviewForm, UserProfileForm, RoomUpdateForm

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
            user = form.save()  # Simpan pengguna baru
            # Buat UserProfile untuk pengguna tersebut
            UserProfile.objects.create(user=user)
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
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Jika profil tidak ada, arahkan ke halaman edit profil
        messages.error(request, 'Please complete your profile information.')
        return redirect('edit_profile')  # Arahkan ke halaman edit profil

    return render(request, 'homestay/profile.html', {'profile': profile})

# Edit Profile
@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'homestay/edit_profile.html', {'form': form})

# Booking Create View
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'homestay/booking_form.html'

    def form_valid(self, form):
        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        if room.availability:
            form.instance.room = room
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            messages.error(self.request, 'This room is not available.')
            return redirect('room_detail', pk=room.pk)

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
        context['rooms'] = Room.objects.filter(homestay=homestay)
        context['reviews'] = Review.objects.filter(homestay=homestay).order_by('-created_at')
        return context

# Add Review View
class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'homestay/add_review.html'

    def form_valid(self, form):
        homestay = get_object_or_404(Homestay, pk=self.kwargs['pk'])
        form.instance.homestay = homestay
        form.instance.user = self.request.user
        messages.success(self.request, 'Your review has been posted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homestay_detail', kwargs={'pk': self.kwargs['pk']})

# Homestay Create View (CBV)
class HomestayCreateView(LoginRequiredMixin, CreateView):
    model = Homestay
    fields = ['name', 'location', 'description', 'price', 'image']
    template_name = 'homestay/homestay_form.html'
    success_url = reverse_lazy('homestays')  # After success, redirect to homestay list page

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Assign the current user as the owner of the homestay
        return super().form_valid(form)

# Edit Room View
@login_required
def edit_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('profile')  # atau halaman lain jika profil tidak ada

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # redirect ke halaman profil setelah update
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})