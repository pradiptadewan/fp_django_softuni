from django.contrib import admin
from .models import Room, Homestay, Booking, Review, UserProfile, Facility, Location

# Menambahkan Room Model ke Admin
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'homestay', 'price', 'availability')  # Menampilkan kolom-kolom yang diinginkan
    list_filter = ('availability', 'homestay')  # Filter berdasarkan ketersediaan atau homestay
    search_fields = ('name', 'homestay__name')  # Pencarian berdasarkan nama kamar atau homestay

    # Menentukan hak akses berdasarkan role pengguna
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser dapat melihat semua data
        elif request.user.is_staff:
            return queryset.filter(availability=True)  # Staff hanya melihat kamar yang tersedia
        else:
            return queryset.none()  # Pengguna biasa tidak dapat melihat data

# Menambahkan Homestay Model ke Admin
class HomestayAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'description', 'created_at')  # Menampilkan kolom-kolom yang diinginkan
    search_fields = ('name', 'address')  # Pencarian berdasarkan nama atau alamat
    filter_horizontal = ('facilities',)  # Menambahkan antarmuka untuk memilih fasilitas dalam Homestay

    # Menentukan hak akses berdasarkan role pengguna
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser dapat melihat semua data
        elif request.user.is_staff:
            return queryset  # Staff dapat melihat semua data homestay
        else:
            return queryset.none()  # Pengguna biasa tidak dapat melihat data

# Menambahkan Booking Model ke Admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'check_in', 'check_out', 'status']  # Sesuaikan dengan field yang ada
    list_filter = ['check_in', 'check_out']  # Sesuaikan dengan field yang ada
    ordering = ['check_in']  # Sesuaikan dengan field yang ada
    date_hierarchy = 'check_in'  # Sesuaikan dengan field yang ada

    # Menentukan hak akses berdasarkan role pengguna
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser dapat melihat semua data
        elif request.user.is_staff:
            return queryset.filter(status='confirmed')  # Staff hanya dapat melihat pemesanan yang dikonfirmasi
        else:
            return queryset.none()  # Pengguna biasa tidak dapat melihat data

# Menambahkan Review Model ke Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'homestay', 'rating', 'created_at')  # Menampilkan kolom-kolom yang diinginkan
    list_filter = ('rating', 'homestay')  # Filter berdasarkan rating atau homestay
    search_fields = ('user__username', 'homestay__name')  # Pencarian berdasarkan username user atau nama homestay

    # Menentukan hak akses berdasarkan role pengguna
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser dapat melihat semua data
        elif request.user.is_staff:
            return queryset  # Staff dapat melihat semua ulasan
        else:
            return queryset.none()  # Pengguna biasa tidak dapat melihat data

# Menambahkan UserProfile Model ke Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')  # Menampilkan field yang ada di model
    search_fields = ('user__username',)  # Pencarian berdasarkan username user

    # Menentukan hak akses berdasarkan role pengguna
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser dapat melihat semua data
        elif request.user.is_staff:
            return queryset  # Staff dapat melihat profil pengguna
        else:
            return queryset.none()  # Pengguna biasa tidak dapat melihat data

# Menambahkan Facility Model ke Admin
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')  # Menampilkan kolom-kolom yang diinginkan
    search_fields = ('name',)  # Pencarian berdasarkan nama fasilitas

    # Menentukan hak akses berdasarkan role pengguna
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser dapat melihat semua data
        elif request.user.is_staff:
            return queryset  # Staff dapat melihat semua fasilitas
        else:
            return queryset.none()  # Pengguna biasa tidak dapat melihat data

# Menambahkan Location Model ke Admin
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'latitude', 'longitude', 'created_at')  # Menampilkan kolom-kolom yang diinginkan
    search_fields = ('city', 'address')  # Pencarian berdasarkan kota atau alamat

    # Menentukan hak akses berdasarkan role pengguna
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superuser dapat melihat semua data
        elif request.user.is_staff:
            return queryset  # Staff dapat melihat semua lokasi
        else:
            return queryset.none()  # Pengguna biasa tidak dapat melihat data

# Mendaftarkan model ke admin site
admin.site.register(Room, RoomAdmin)
admin.site.register(Homestay, HomestayAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Location, LocationAdmin)
