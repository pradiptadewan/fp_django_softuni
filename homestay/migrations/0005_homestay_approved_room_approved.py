# Generated by Django 5.1.3 on 2024-12-15 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homestay', '0004_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homestay',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
