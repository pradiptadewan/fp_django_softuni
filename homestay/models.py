from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse


# Model untuk Facility
class Facility(models.Model):
    """
    Model untuk menyimpan informasi tentang fasilitas yang tersedia di homestay.
    """
    name = models.CharField(max_length=100, unique=True)  # Nama fasilitas (unik)
    description = models.TextField(blank=True, null=True)  # Deskripsi opsional
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal dibuat otomatis

    def __str__(self):
        return self.name


# Model untuk Location
class Location(models.Model):
    """
    Model untuk menyimpan informasi lokasi homestay, termasuk koordinat.
    """
    city = models.CharField(max_length=100)  # Kota lokasi
    address = models.TextField()  # Alamat lengkap
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Koordinat latitude
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Koordinat longitude
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal dibuat otomatis

    def __str__(self):
        return f"{self.city} - {self.address}"


# Model untuk Homestay
class Homestay(models.Model):
    """
    Model untuk menyimpan informasi tentang homestay, termasuk fasilitas dan lokasi.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='homestays/')
    facilities = models.ManyToManyField(Facility, blank=True)  # Relasi ManyToMany ke Facility
    location = models.OneToOneField(Location, on_delete=models.CASCADE, blank=True, null=True)  # Relasi OneToOne ke Location
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('homestay_detail', args=[self.slug])


# Model untuk Room
class Room(models.Model):
    """
    Model untuk menyimpan informasi tentang kamar di homestay, termasuk harga, kapasitas, dan status ketersediaan.
    """
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='rooms/')
    number_of_guests = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('room_detail', args=[self.slug])


# Model untuk Booking
class Booking(models.Model):
    """
    Model untuk menyimpan informasi pemesanan kamar oleh pengguna, termasuk status dan tanggal pemesanan.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guest_count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, default='pending', choices=[(
        'pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ])

    def __str__(self):
        return f"Booking for {self.room} by {self.user}"

    def clean(self):
        """
        Validasi agar tanggal check-out lebih besar dari tanggal check-in.
        """
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after check-in date.")

    def save(self, *args, **kwargs):
        """
        Override save untuk memastikan status 'approved' mengubah status ketersediaan kamar.
        """
        self.clean()
        if self.status == 'approved' and self.room.availability:
            self.room.availability = False  # Menandai kamar tidak tersedia jika sudah disetujui
            self.room.save()
        super().save(*args, **kwargs)


# Model untuk Review
class Review(models.Model):
    """
    Model untuk menyimpan review dari pengguna mengenai homestay, termasuk rating dan komentar.
    """
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.homestay} by {self.user}"

    def clean(self):
        """
        Validasi agar pengguna hanya bisa memberikan satu review per homestay.
        """
        if Review.objects.filter(user=self.user, homestay=self.homestay).exists():
            raise ValidationError("User has already reviewed this homestay.")

    def save(self, *args, **kwargs):
        """
        Override save untuk memvalidasi review sebelum disimpan.
        """
        self.clean()
        super().save(*args, **kwargs)


# Model untuk UserProfile

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username