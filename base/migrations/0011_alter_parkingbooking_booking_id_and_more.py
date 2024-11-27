# Generated by Django 5.0.7 on 2024-11-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_parkingbooking_booking_id_parkingbooking_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingbooking',
            name='booking_id',
            field=models.CharField(default='', editable=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='parkingbooking',
            name='qr_code',
            field=models.ImageField(default='', editable=False, unique=True, upload_to='parking_qr_codes/'),
        ),
    ]
