import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import datetime


def set_default_created_at(apps, schema_editor):
    Homestay = apps.get_model('homestay', 'Homestay')
    for homestay in Homestay.objects.filter(created_at__isnull=True):
        homestay.created_at = datetime.datetime.now()  # Atau gunakan waktu lain sesuai keinginan
        homestay.save()


class Migration(migrations.Migration):
    dependencies = [
        ('homestay', '0002_homestay_booking_number_of_guests_booking_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Mengubah field 'created_at' tanpa memberikan default secara manual
        migrations.AddField(
            model_name='homestay',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),

        # Mengubah field pada model 'booking'
        migrations.AlterField(
            model_name='booking',
            name='number_of_guests',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('approved', 'Approved'), ('cancelled', 'Cancelled')],
                default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='room',
            name='number_of_guests',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),

        # Membuat model UserProfile
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),

        # Menambahkan operasi untuk mengatur nilai default untuk created_at pada data lama
        migrations.RunPython(set_default_created_at),
    ]
