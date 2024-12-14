from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify


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
    address = models.CharField(max_length=255, default='unknown')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='homestays/')
    facilities = models.ManyToManyField(Facility, blank=True)  # Relasi ManyToMany ke Facility
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)  # Relasi OneToOne ke Location
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

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
    slug = models.SlugField(max_length=150, unique=True, blank=True)  # Izinkan slug kosong saat input
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='rooms/', default='homestay/images/g1.jpg' , blank=True, null=True)
    number_of_guests = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = slugify(self.name)
            count = 1
            while Room.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slugify(self.name)}-{count}"
                count += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('room_detail', args=[self.slug])


# Model untuk Booking
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room.name}"



# Model untuk Review
class Review(models.Model):
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)  # Menambahkan kolom homestay
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.homestay} by {self.user}"

    def save(self, *args, **kwargs):
        # Validasi dilakukan sebelum menyimpan
        if not self.user:
            raise ValueError('User is required for the review.')
        super().save(*args, **kwargs)


# Model untuk UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
