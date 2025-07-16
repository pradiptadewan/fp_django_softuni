from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    home, about, contact,
    RoomListView, RoomDetailView,
    BookingCreateView, booking_confirm,
    UserBookingListView,
    HomestayListView, HomestayDetailView, HomestayCreateView,
    AddReviewView,
    register, login_view, logout_view, profile, edit_profile, get_rooms_by_homestay
)

urlpatterns = [
    # Halaman Utama dan Informasi Umum
    path('', home, name='home'),  # Halaman utama
    path('about/', about, name='about'),  # Halaman about
    path('contact/', contact, name='contact'),  # Halaman contact

    # Rooms
    path('rooms/', login_required(RoomListView.as_view()), name='rooms'),  # Daftar kamar
    path('rooms/<int:pk>/', login_required(RoomDetailView.as_view()), name='room_detail'),  # Detail kamar
    path('homestay/<int:homestay_id>/create_room/', views.create_room, name='create_room'), #Membuat Kamar
    path('get_room_image/<int:room_id>/', views.get_room_image, name='get_room_image'),

    # User Authentication
    path('register/', register, name='register'),  # Halaman registrasi
    path('login/', login_view, name='login'),  # Halaman login
    path('logout/', logout_view, name='logout'),  # Halaman logout
    path('profile/', login_required(profile), name='profile'),  # Profil pengguna (login diperlukan)
    path('edit_profile/', login_required(edit_profile), name='edit_profile'),  # Use edit_profile here

    # Password Reset URLs
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # URL untuk reset password
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # URL setelah permintaan reset
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # URL untuk konfirmasi password reset
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # URL setelah reset selesai

    # Booking
    path('booking/<int:pk>/', login_required(BookingCreateView.as_view()), name='booking_form'),  # Form booking
    path('booking/confirm/', login_required(booking_confirm), name='booking_confirm'),  # Konfirmasi booking
    path('bookings/', login_required(UserBookingListView.as_view()), name='bookings'),  # Daftar booking pengguna (login diperlukan)
    path('room/<int:pk>/book/', BookingCreateView.as_view(), name='booking_create'),
    path('booking/<int:pk>/confirm/', booking_confirm, name='booking_confirm'),
    path('get_rooms_by_homestay/<int:homestay_id>/', get_rooms_by_homestay, name='get_rooms_by_homestay'),

    #PAYMENT
    path('payment/<int:booking_id>/', views.PaymentView.as_view(), name='payment'),

    #CANCEL
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('check_out_booking/<int:booking_id>/', views.check_out_booking, name='check_out_booking'),

    # Homestays
    path('homestays/', login_required(HomestayListView.as_view()), name='homestays'),  # Daftar homestay
    path('homestays/<int:pk>/', login_required(HomestayDetailView.as_view()), name='homestay_detail'),  # Detail homestay
    path('homestays/<int:pk>/add_review/', login_required(AddReviewView.as_view()), name='add_review'),  # Tambah review
    path('homestays/create/', login_required(HomestayCreateView.as_view()), name='homestay_create'),  # Create homestay

    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/homestay/edit/<int:pk>/', views.edit_homestay, name='edit_homestay'),
    path('staff/homestay/delete/<int:pk>/', views.delete_homestay, name='delete_homestay'),
    path('staff/room/edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('staff/room/delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('booking/detail/<int:booking_id>/', views.view_booking, name='view_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
