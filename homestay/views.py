from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking, Room, Review, UserProfile
from .form import BookingForm, RegisterForm, ReviewForm, UserProfileForm, RoomForm
from .models import Homestay, ContactMessage
from .form import HomestayForm
from django.http import JsonResponse
from django.utils import timezone




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
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Thank you for reaching out! We will get back to you shortly.")

        return redirect("contact")

    return render(request, "homestay/contact.html")

# Register User
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
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

                if request.POST.get('remember'):
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
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
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile information.')
        return redirect('edit_profile')
    return render(request, 'homestay/profile.html', {'profile': user_profile})

# Booking Create View
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'homestay/booking_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment', kwargs={'booking_id': self.object.id})

def get_rooms_by_homestay(request, homestay_id):
    rooms = Room.objects.filter(homestay_id=homestay_id)
    room_list = [{'id': room.id, 'name': room.name} for room in rooms]
    return JsonResponse({'rooms': room_list})

def get_room_image(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        image_url = room.image.url if room.image else None
        return JsonResponse({'image_url': image_url})
    except Room.DoesNotExist:
        return JsonResponse({'image_url': None})

def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'homestay/booking_confirm.html', {'booking': booking})

#PAYMENT
class PaymentView(TemplateView):
    template_name = 'homestay/payment.html'

    def get_context_data(self, **kwargs):
        booking_id = self.kwargs['booking_id']
        booking = Booking.objects.get(id=booking_id)

        context = super().get_context_data(**kwargs)
        context['booking'] = booking
        return context

    def post(self, request, *args, **kwargs):
        # Ambil ID booking dari URL
        booking_id = self.kwargs['booking_id']
        booking = Booking.objects.get(id=booking_id)

        # Misalnya, kita lakukan pembayaran dan ubah status pemesanan
        booking.status = 'Booked'  # Ubah status booking
        booking.save()

        # Tambahkan pesan sukses
        messages.success(request, 'Payment successful! Your booking is now confirmed.')

        # Redirect ke halaman konfirmasi setelah pembayaran
        return redirect('booking_confirm', pk=booking.id)

#CANCEL
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.user != request.user:
        messages.error(request, 'You cannot cancel this booking.')
        return redirect('bookings')

    if booking.check_in < timezone.now().date():
        messages.error(request, 'You cannot cancel a booking after the check-in date.')
        return redirect('bookings')

    booking.delete()

    messages.success(request, 'Your booking has been successfully cancelled.')
    return redirect('bookings')

# User Bookings List View
class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'homestay/bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

def view_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'homestay/booking_detail.html', {'booking': booking})

# Homestay Create View (CBV)
class HomestayCreateView(LoginRequiredMixin, CreateView):
    model = Homestay
    form_class = HomestayForm
    template_name = 'homestay/homestay_form.html'
    success_url = reverse_lazy('homestays')  # Redirect ke daftar homestay setelah berhasil

    def form_valid(self, form):

        form.instance.owner = self.request.user
        response = super().form_valid(form)

        if 'facilities' in form.cleaned_data:
            form.instance.facilities.set(form.cleaned_data['facilities'])

        return response

# Homestay List View
class HomestayListView(ListView):
    model = Homestay
    template_name = 'homestay/homestays.html'
    context_object_name = 'homestays'

    def get_queryset(self):
        return Homestay.objects.filter(approved=True)

# Homestay Detail View
class HomestayDetailView(DetailView):
    model = Homestay
    template_name = 'homestay/homestay_detail.html'
    context_object_name = 'homestay'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homestay = self.get_object()

        context['rooms'] = Room.objects.filter(homestay=homestay, approved=True)

        context['reviews'] = Review.objects.filter(homestay=homestay).order_by('-created_at')
        context['facilities'] = homestay.facilities.all()

        return context


# Add Review View
class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'homestay/add_review.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homestay'] = get_object_or_404(Homestay, pk=self.kwargs['pk'])
        return context
    def form_valid(self, form):
        homestay_id = form.cleaned_data['homestay']  # Ambil homestay_id dari form
        homestay = get_object_or_404(Homestay, pk=homestay_id)
        form.instance.homestay = homestay
        form.instance.user = self.request.user

        if Review.objects.filter(user=self.request.user, homestay=homestay).exists():
            messages.error(self.request, 'You have already posted a review for this homestay.')
            return redirect('homestay_detail', pk=homestay.pk)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('homestay_detail', kwargs={'pk': self.kwargs['pk']})

@login_required
def edit_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            # Update user info
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')

            password = request.POST.get('password')
            if password:
                user.set_password(password)

            user.save()
            form.save()

            if password:
                update_session_auth_hash(request, user)

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect ke halaman profil setelah update berhasil
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'homestay/edit_profile.html', {'user': user, 'form': form})


@login_required
def add_review(request, homestay_id):
    homestay = get_object_or_404(Homestay, id=homestay_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.homestay = homestay
            review.save()
            return redirect('homestay:detail', homestay_id=homestay.id)
    else:
        form = ReviewForm()

    return render(request, 'homestay/add_review.html', {'form': form, 'homestay': homestay})

@login_required
def create_room(request, homestay_id):
    homestay = Homestay.objects.get(id=homestay_id)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.homestay = homestay
            room.save()
            return redirect('homestay_detail', pk=homestay.id)
    else:
        form = RoomForm()

    return render(request, 'homestay/create_room.html', {'form': form, 'homestay': homestay})


# Staff Dashboard
@login_required
def staff_dashboard(request):
    if not request.user.groups.filter(name='Staff').exists():
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    homestays = Homestay.objects.all()
    rooms = Room.objects.all()
    bookings = Booking.objects.all()

    status_filter = request.GET.get('status', None)
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    order = request.GET.get('order', 'desc')  # Default pengurutan berdasarkan tanggal terbaru

    if order == 'desc':
        bookings = bookings.order_by('-check_in')
    elif order == 'asc':
        bookings = bookings.order_by('check_in')

    return render(request, 'homestay/staff_dashboard.html', {
        'homestays': homestays,
        'rooms': rooms,
        'bookings': bookings
    })

def check_out_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status == 'Booked':
        booking.status = 'Checked Out'
        booking.save()
        messages.success(request, f'Booking {booking.id} has been checked out successfully.')
    else:
        messages.error(request, f'Booking {booking.id} cannot be checked out because it is already {booking.status}.')

    return redirect('staff_dashboard')


# Edit Homestay View
@login_required
def edit_homestay(request, pk):
    homestay = get_object_or_404(Homestay, pk=pk)

    if not request.user.groups.filter(name='Staff').exists():
        messages.error(request, "You do not have permission to edit this homestay.")
        return redirect('home')

    if request.method == 'POST':
        form = HomestayForm(request.POST, instance=homestay)
        if form.is_valid():
            form.save()
            messages.success(request, 'Homestay updated successfully!')
            return redirect('staff_dashboard')
    else:
        form = HomestayForm(instance=homestay)

    return render(request, 'homestay/edit_homestay.html', {'form': form})

# Delete Homestay View
@login_required
def delete_homestay(request, pk):
    homestay = get_object_or_404(Homestay, pk=pk)

    if not request.user.groups.filter(name='Staff').exists():
        messages.error(request, "You do not have permission to delete this homestay.")
        return redirect('home')

    homestay.delete()
    messages.success(request, 'Homestay deleted successfully!')
    return redirect('staff_dashboard')

# Edit Room View
@login_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if not request.user.groups.filter(name='Staff').exists():
        messages.error(request, "You do not have permission to edit this room.")
        return redirect('home')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('staff_dashboard')
    else:
        form = RoomForm(instance=room)

    return render(request, 'homestay/edit_room.html', {'form': form})

# Delete Room View
@login_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if not request.user.groups.filter(name='Staff').exists():
        messages.error(request, "You do not have permission to delete this room.")
        return redirect('home')

    room.delete()
    messages.success(request, 'Room deleted successfully!')
    return redirect('staff_dashboard')

def cancel_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Cancelled'
    booking.save()

    messages.success(request, 'Successful Cancellation of Booking.')
    return redirect('staff_dashboard')

def delete_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    booking.delete()

    return redirect('staff_dashboard')
