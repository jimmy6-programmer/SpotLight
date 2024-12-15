from django.db import models
import uuid
import qrcode
from django.core.files import File
from io import BytesIO
from django.core.validators import RegexValidator
from django.db import models
import africastalking
from django.conf import settings
import re
from django.utils.crypto import get_random_string

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Perfomer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="perfomers/")
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=False, blank=False)
    money_per_hour = models.IntegerField(null=True, blank=True)
    video_highlight = models.URLField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    security_code = models.CharField(max_length=8, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.security_code:
            self.security_code = str(uuid.uuid4())  # Generates a unique 8-character code
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.artist_name
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    banner = models.ImageField(upload_to="events/")
    
    def __str__(self):
        return self.name
       
class Ticket(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    number_of_ticket=models.IntegerField(default="0")
    
class ParkingLot(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='parking_lots')
    lot_number = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Parking Lot {self.lot_number} for {self.event.name}"
    
class ParkingBooking(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='bookings')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=10, choices=[('MTN', 'MTN'), ('Airtel', 'Airtel')])
    booked_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='parking_qr_codes/', blank=True, editable=False, null=True)

    def __str__(self):
        return f"Booking for {self.firstname} {self.lastname} - Lot {self.parking_lot.lot_number}"

    def save(self, *args, **kwargs):
        if not self.qr_code:  # Only generate if `qr_code` is not set
            qr_data = (
                f"Booking ID: {self.id}\n"
                f"Name: {self.firstname} {self.lastname}\n"
                f"Phone Number: {self.telephone}\n"
                f"Event: {self.parking_lot.event.name}\n"
                f"Parking Lot: {self.parking_lot.lot_number}\n"
                f"Date: {self.parking_lot.event.date.strftime('%Y-%m-%d %H:%M')}"
            )

            qr_image = qrcode.make(qr_data)
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')

            # Generate a unique filename
            filename = f"{self.id}_qr_code.png"

            # Save the QR code image to the field
            self.qr_code.save(filename, File(buffer), save=False)
            
        super().save(*args, **kwargs)
    
    
PAYMENT_CHOICES = [
    ('MTN', 'MTN MoMo'),
    ('Airtel', 'Airtel Money'),
]    

class Checkout(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()

    # Phone number validation
    phone_number_validator = RegexValidator(
        regex=r'^(078|079|072|073)\d{7}$',
        message="Phone number must start with 078, 079, 072, or 073 and be 10 digits long."
    )
    phonenumber = models.CharField(
        max_length=10,
        validators=[phone_number_validator],
        help_text="Enter a valid phone number starting with 078, 079, 072, or 073."
    )
    
    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, editable=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    purchased_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            # Generate a unique ticket ID
            self.ticket_id = f"tick{uuid.uuid4().hex[:8]}"
        
        super().save(*args, **kwargs)

        # Format the QR code data as a simple string without JSON
        qr_data = (
            f"Ticket ID: {self.ticket_id}\n"
            f"Name: {self.firstname} {self.lastname}\n"
            f"Email: {self.email}\n"
            f"Phone Number: {self.phonenumber}\n"
            f"Event: {self.event.name}\n"
            f"Ticket Type: {self.purchased_ticket.name}\n"
            f"Date: {self.event.date.strftime('%Y-%m-%d %H:%M')}"
        )
        
        # Generate the QR code from the formatted string
        qr_image = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        
        # Save the QR code image
        self.qr_code.save(f"{self.ticket_id}.png", File(buffer), save=False)
        
        super().save(*args, **kwargs)  # Save again to update the QR code

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
 
DURATION_UNITS = [
    ('hours', 'Hours'),
    ('minutes', 'Minutes'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ]    
    
class Invitation(models.Model):
    performer = models.ForeignKey(Perfomer, on_delete=models.CASCADE, related_name="invitations")
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    invite_performer_on = models.DateTimeField(null=True)  # When the performer is invited
    location = models.CharField(max_length=255, null=True)  # Location of the event
    duration = models.DecimalField(null=True, max_digits=9999999999999999, decimal_places=2)  # Duration in hours
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNITS, default='hours', null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total calculated amount
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', null=True) 
    
    def save(self, *args, **kwargs):
        if self.performer and self.performer.money_per_hour is not None:
            duration_in_hours = self.duration
            if self.duration_unit == 'minutes':
                duration_in_hours = self.duration / 60  # Preserve fractional hours
            self.total_amount = self.performer.money_per_hour * duration_in_hours
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invitation to {self.performer.artist_name} by {self.name}"  

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
           
class Sponsor(models.Model):
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/')
    telephone = models.IntegerField(max_length=10)
    paid = models.BooleanField(default=False)           
    
class Video(models.Model):
    performer = models.ForeignKey(Perfomer, related_name="videos", on_delete=models.CASCADE)
    video_url = models.URLField()
    
    def __str__(self):
        return f"video for {self.performer.artist_name}"    
    
    def get_embedded_url(self):
        """Extracts YouTube video ID and returns the embeddable URL."""
        if "v=" in self.video_url:
            try:
                video_id = self.video_url.split('v=')[1].split('&')[0]
                return f"https://www.youtube.com/embed/{video_id}"
            except IndexError:
                return None
        elif "youtube.com/embed/" in self.video_url:
            return self.video_url
        elif "youtube.com/v/" in self.video_url:
            video_id = self.video_url.split("youtube.com/v/")[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return None

class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def send_sms_to_all(self):
        # Initialize Africa's Talking SDK
        africastalking.initialize(
            username=settings.AFRICASTALKING_USERNAME,  # Sandbox or live username
            api_key=settings.AFRICASTALKING_API_KEY     # Your API key
        )

        recipients = ['+250794686625','+250790912004', '+250788565439']             
        # Create an SMS service instance
        sms = africastalking.SMS

        try:
            # Send the SMS
            response = sms.send(self.message, recipients)
            print("SMS sent successfully:", response)
        except Exception as e:
            print(f"Error sending SMS: {e}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Send SMS after saving the notification
        self.send_sms_to_all()
        
class Advertisement(models.Model): 
    name = models.CharField(max_length=255) 
    link = models.URLField(blank=True, null=True)
    video = models.FileField(upload_to='ads/', max_length=200) 

    def __str__(self):
        return self.name     
    
    
class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='banners/')
    button_text_1 = models.CharField(max_length=50, default='Get Ticket')
    button_url_1 = models.URLField()
    button_text_2 = models.CharField(max_length=50, default='Know More')
    button_url_2 = models.URLField()

    def __str__(self):
        return self.title