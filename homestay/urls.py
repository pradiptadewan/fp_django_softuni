from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Halaman utama
    path('about/', views.about, name='about'),
    path('rooms/', views.rooms_list, name='rooms'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Booking
    path('booking/<int:room_id>/', views.booking_form, name='booking_form'),
    path('booking/confirm/', views.booking_confirm, name='booking_confirm'),
    path('bookings/', views.bookings, name='bookings'),

    # Homestay
    path('homestays/', views.homestays_list, name='homestays'), # Daftar homestay
    path('homestays/<int:pk>/', views.homestay_detail, name='homestay_detail'),
    path('homestays/<int:homestay_id>/add_review/', views.add_review, name='add_review'),

]