from django.db import models
from django.contrib.auth.models import User

# Model untuk Homestay
class Homestay(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='homestays/')
    def __str__(self):
        return self.name

# Model untuk Room
class Room(models.Model):
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE) # Hubungan ke Homestay
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='rooms/')
    number_of_guests = models.IntegerField()  # Menentukan kapasitas maksimal
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Model untuk Booking
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.IntegerField()
    status = models.CharField(max_length=20, default='pending') # Menambahkan status

    def __str__(self):
        return f"Booking for {self.room} by {self.user}"

    def save(self, *args, **kwargs):
        # Atur ketersediaan ruangan
        self.room.availability = False
        self.room.save()
        super().save(*args, **kwargs)

# Model untuk Review
class Review(models.Model):
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review for {self.homestay} by {self.user}"