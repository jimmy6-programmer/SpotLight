from django import forms
from base.models import Invitation, Checkout, Sponsor, ParkingLot
from django import forms
from .models import Contact


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
        
     

