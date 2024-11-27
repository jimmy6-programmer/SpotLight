# your_app_name/migrations/XXXX_populate_qr_codes.py
from django.db import migrations

def generate_qr_codes(apps, schema_editor):
    ParkingBooking = apps.get_model('base', 'ParkingBooking')
    for booking in ParkingBooking.objects.filter(qr_code__isnull=True):
        booking.save()  # Triggers the `save()` method to generate QR code

class Migration(migrations.Migration):
    dependencies = [
        ('base', '0016_alter_parkingbooking_qr_code'),  # Adjust to the last migration name
    ]

    operations = [
        migrations.RunPython(generate_qr_codes),
    ]
