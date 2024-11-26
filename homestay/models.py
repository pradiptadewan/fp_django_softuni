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
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE,
                                 related_name='rooms')  # Mempermudah akses ke rooms dari homestay
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
    number_of_guests = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='pending')  # Menambahkan status pemesanan

    def __str__(self):
        return f"Booking for {self.room} by {self.user}"

    def save(self, *args, **kwargs):
        # Validasi check-in dan check-out
        if self.check_in >= self.check_out:
            raise ValueError("Check-out date must be after check-in date.")

        # Atur ketersediaan ruangan hanya jika status booking adalah 'approved'
        if self.status == 'approved' and self.room.availability:
            self.room.availability = False  # Mengubah status availability
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

    def clean(self):
        # Pastikan rating hanya berada dalam rentang 1-5
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

    def save(self, *args, **kwargs):
        # Cek apakah sudah ada review oleh pengguna yang sama untuk homestay yang sama
        if Review.objects.filter(user=self.user, homestay=self.homestay).exists():
            raise ValueError("User has already reviewed this homestay.")

        self.clean()  # Jalankan validasi rating
        super().save(*args, **kwargs)
