# Generated by Django 5.0.7 on 2024-11-16 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_remove_parkingbooking_booking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingbooking',
            name='qr_code',
            field=models.ImageField(default='', editable=False, upload_to='parking_qr_codes/'),
        ),
    ]
