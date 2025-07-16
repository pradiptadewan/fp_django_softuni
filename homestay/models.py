from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from datetime import timedelta


# Model untuk Facility
class Facility(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Model untuk Location
class Location(models.Model):

    city = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.address}"


# Model untuk Homestay
class Homestay(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=255, default='unknown')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='homestays/')
    facilities = models.ManyToManyField(Facility, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('homestay_detail', args=[self.slug])



# Model untuk Room
class Room(models.Model):

    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='rooms/', default='homestay/images/g1.jpg' , blank=True, null=True)
    number_of_guests = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    availability = models.BooleanField(default=True)

    approved = models.BooleanField(default=False)

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
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=[('Booked', 'Booked'), ('Cancelled', 'Cancelled'),
                                                      ('Checked Out', 'Checked Out')],
                              default='Booked')


    @property
    def total_price(self):
        duration = (self.check_out - self.check_in).days
        room_price = self.room.price
        return room_price * duration

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room.name}"



# Model untuk Review
class Review(models.Model):
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.homestay} by {self.user}"

    def save(self, *args, **kwargs):

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

# Menyimpan Kontak
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"


