from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking, Room, Review, UserProfile
from .form import BookingForm, RegisterForm, ReviewForm, UserProfileForm, RoomForm
from .models import Homestay, ContactMessage
from .form import HomestayForm

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

        # Simpan data ke database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Tampilkan pesan sukses
        messages.success(request, "Thank you for reaching out! We will get back to you shortly.")

        # Redirect ke halaman "Contact Us" atau halaman lain
        return redirect("contact")

    return render(request, "homestay/contact.html")

# Register User
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Simpan pengguna baru
            # Buat UserProfile untuk pengguna tersebut
            UserProfile.objects.create(user=user)
            # Menampilkan pesan sukses
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect ke halaman login setelah registrasi berhasil
    else:
        form = RegisterForm()

    # Render halaman registrasi dengan form
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
        # Mencari profil pengguna yang sedang login
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Jika profil tidak ada, arahkan ke halaman edit profil
        messages.error(request, 'Please complete your profile information.')
        return redirect('edit_profile')  # Arahkan ke halaman edit profil

    return render(request, 'homestay/profile.html', {'profile': user_profile})

# Booking Create View
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'homestay/booking_form.html'

    def form_valid(self, form):
        # Tetapkan pengguna yang sedang login
        form.instance.user = self.request.user

        # Ambil data kamar berdasarkan primary key (pk)
        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        form.instance.room = room

        # Hitung total harga berdasarkan lama tinggal
        days_stay = (form.cleaned_data['check_out'] - form.cleaned_data['check_in']).days
        form.instance.total_price = room.price * days_stay

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('booking_confirm', kwargs={'pk': self.object.pk})

# Booking Confirmation
def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'homestay/booking_confirm.html', {'booking': booking})


# User Bookings List View
class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'homestay/bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


# Homestay Create View (CBV)
class HomestayCreateView(LoginRequiredMixin, CreateView):
    model = Homestay
    form_class = HomestayForm
    template_name = 'homestay/homestay_form.html'
    success_url = reverse_lazy('homestays')  # Redirect ke daftar homestay setelah berhasil

    def form_valid(self, form):
        # Tetapkan pemilik homestay ke pengguna yang sedang login
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Menyimpan fasilitas yang dipilih (ManyToMany)
        if 'facilities' in form.cleaned_data:
            form.instance.facilities.set(form.cleaned_data['facilities'])

        return response

# Homestay List View
class HomestayListView(ListView):
    model = Homestay
    template_name = 'homestay/homestays.html'
    context_object_name = 'homestays'

    def get_queryset(self):
        # Hanya menampilkan homestay yang sudah disetujui
        return Homestay.objects.filter(approved=True)

# Homestay Detail View
class HomestayDetailView(DetailView):
    model = Homestay
    template_name = 'homestay/homestay_detail.html'
    context_object_name = 'homestay'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homestay = self.get_object()

        # Hanya menampilkan rooms yang sudah disetujui
        context['rooms'] = Room.objects.filter(homestay=homestay, approved=True)

        # Menambahkan review dan fasilitas terkait homestay
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
        # Validasi jika review sudah ada
        if Review.objects.filter(user=self.request.user, homestay=homestay).exists():
            messages.error(self.request, 'You have already posted a review for this homestay.')
            return redirect('homestay_detail', pk=homestay.pk)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('homestay_detail', kwargs={'pk': self.kwargs['pk']})

@login_required
def edit_profile(request):
    user = request.user
    # Mengambil data profil pengguna (jika ada)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Menggunakan form untuk menangani pembaruan data
        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            # Update user info
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')

            # Update password jika ada
            password = request.POST.get('password')
            if password:
                user.set_password(password)

            user.save()

            # Save user profile data
            form.save()

            # Jika password diubah, update session auth hash
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
            review.user = request.user  # Mengatur user yang memberikan review
            review.homestay = homestay  # Menghubungkan review dengan homestay
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