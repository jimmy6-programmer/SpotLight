from django import forms
from base.models import Invitation, Checkout, Sponsor, ParkingLot, Perfomer, Category
from django import forms
from .models import Contact
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['name', 'telephone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your telephone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here',
                'rows': 4  # Adjust rows for height if needed
            }),
        }        
        
class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('MTN', 'MTN MoMo'),
        ('Airtel', 'Airtel Money'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        label="Payment Method"
    )
    class Meta:
        model = Checkout
        fields = ['firstname', 'lastname', 'email', 'phonenumber', 'payment_method']   
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your First name'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phonenumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write your Phone number',
                'rows': 4  # Adjust rows for height if needed
            }),
        }     

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}),
        }
        
     
class PerfomerRegistrationForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label="Select a Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Perfomer
        fields = [
            'first_name', 'last_name', 'artist_name', 'gender', 'description',
            'category', 'image', 'facebook', 'twitter', 'instagram', 
            'email', 'telephone','money_per_hour', 'video_highlight'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'artist_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artist Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe yourself', 'rows': 4}),
            'money_per_hour': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Money per hour (optional)'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Profile URL'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter Profile URL'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Profile URL'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}),
            'video_highlight': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Video Highlight URL'}),
        }

    def clean_facebook(self):
        return self.validate_social_url('facebook.com', self.cleaned_data.get('facebook'))

    def clean_twitter(self):
        return self.validate_social_url('twitter.com', self.cleaned_data.get('twitter'))

    def clean_instagram(self):
        return self.validate_social_url('instagram.com', self.cleaned_data.get('instagram'))

    @staticmethod
    def validate_social_url(platform, url):
        if url:
            URLValidator()(url)  # Check if it's a valid URL
            if platform not in url:
                raise ValidationError(f"URL must be a valid {platform} link.")
        return url