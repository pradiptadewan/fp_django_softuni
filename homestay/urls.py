from django.urls import path
from . import views
from .views import (
    home, about, contact,
    RoomListView, RoomDetailView,
    BookingCreateView, booking_confirm,
    UserBookingListView,
    HomestayListView, HomestayDetailView,
    AddReviewView,
    register, login_view, logout_view, profile
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Halaman Utama dan Informasi Umum
    path('', home, name='home'),  # Halaman utama
    path('about/', about, name='about'),  # Halaman about
    path('contact/', contact, name='contact'),  # Halaman contact

    # Rooms
    path('rooms/', RoomListView.as_view(), name='rooms'),  # Daftar kamar
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),  # Detail kamar

    # User Authentication
    path('register/', register, name='register'),  # Halaman registrasi
    path('login/', login_view, name='login'),  # Halaman login
    path('logout/', logout_view, name='logout'),  # Halaman logout
    path('profile/', login_required(profile), name='profile'),  # Profil pengguna (login diperlukan)

    # Booking
    path('booking/<int:pk>/', BookingCreateView.as_view(), name='booking_form'),  # Form booking
    path('booking/confirm/', booking_confirm, name='booking_confirm'),  # Konfirmasi booking
    path('bookings/', login_required(UserBookingListView.as_view()), name='bookings'),  # Daftar booking pengguna (login diperlukan)

    # Homestays
    path('homestays/', HomestayListView.as_view(), name='homestays'),  # Daftar homestay
    path('homestays/<int:pk>/', HomestayDetailView.as_view(), name='homestay_detail'),  # Detail homestay
    path('homestays/<int:pk>/add_review/', AddReviewView.as_view(), name='add_review'),  # Tambah review
]
