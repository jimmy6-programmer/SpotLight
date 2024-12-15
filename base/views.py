import html
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from base.models import Perfomer, Category, Event, Ticket, Checkout, Sponsor, ParkingBooking, ParkingLot, Advertisement, Banner, Invitation
from base.forms import InvitationForm, CheckoutForm, PerformerLoginForm
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
import qrcode
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os
import base64
import subprocess
from django.contrib import messages
from .forms import ContactForm, PerfomerRegistrationForm
from django.templatetags.static import static
from django.utils.html import escape
from django.views import View


# Create your views here.
def home(request):
    performers = Perfomer.objects.all()[:8]
    events = Event.objects.all()[:3]
    Advertisements= Advertisement.objects.all()
    paid_sponsors = Sponsor.objects.filter(paid=True)
    banners = Banner.objects.all()
    context = {
        "performers":performers,
        "events":events,
        "paid_sponsors":paid_sponsors,
        "Advertisements":Advertisements,
        "banners":banners,
    }
    return render(request, 'website/index.html',context)

def perfomerdetails(request, id):
    performers = Perfomer.objects.get(pk=id)
    form = InvitationForm()
    
    context = {
        "performers":performers,
        "form":form,
    }
    return render(request, "website/perfomer-details.html" , context)
    

def perfomers(request):
    categories = Category.objects.all()
    performers = Perfomer.objects.filter(approved=True)  

    # Get filter parameters for the request
    category_id = request.GET.get('category')
    name_query = request.GET.get('name')
    
    # Filter perfomers based on selected category if provided
    if category_id:
        performers = performers.filter(category__id=category_id)
        
    # Filter perfomers based on name if provided
    if name_query:
        performers = performers.filter(artist_name__icontains=name_query)    
        
    # Initialize the registration form
    form = PerfomerRegistrationForm()    

    context = {
        "categories": categories,
        "performers": performers,
        "form":form,
    }
    return render(request, 'website/perfomers.html', context)

def invite_performer(request, id):
    performer = get_object_or_404(Perfomer, pk=id)
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.performer = performer
            invitation.save()
            return redirect('perfomers')
        
    else:
        form = InvitationForm()

    return render(request, 'website/perfomer-details.html', {'performer': performer, 'form': form})


def Events(request):
    events = Event.objects.all()
    context = {
        'events':events,
    }
    return render(request, 'website/events.html', context)   

def Tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event=event)
    parking_lots = ParkingLot.objects.filter(event=event, availability=True)

    for ticket in tickets:
        # Count the number of times a ticket has been purchased using the Checkout model
        purchased_count = Checkout.objects.filter(purchased_ticket=ticket).count()
        total_tickets = ticket.number_of_ticket
        remaining_tickets = total_tickets - purchased_count

        # Calculate the percentage of remaining tickets
        if total_tickets > 0:
            percentage_remaining = (remaining_tickets / total_tickets) * 100
        else:
            percentage_remaining = 0

        # Add the calculated fields to each ticket object
        ticket.remaining_tickets = remaining_tickets
        ticket.percentage_remaining = percentage_remaining
        
    if request.method == 'POST':
        # Handle form data for parking lot booking
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phonenumber = request.POST.get('phonenumber')
        payment_method = request.POST.get('payment_method')
        parking_lot_id = request.POST.get('parking_lot_id')
        
        
        print(f"Received parking_lot_id: {parking_lot_id}")
        
        
        if firstname and lastname and phonenumber and payment_method and parking_lot_id:
            parking_lot = get_object_or_404(ParkingLot, id=parking_lot_id, event=event)

            if parking_lot.availability:
                # Create the booking
                booking = ParkingBooking.objects.create(
                    parking_lot=parking_lot,
                    firstname=firstname,
                    lastname=lastname,
                    telephone=phonenumber,
                    payment_method=payment_method
                )

                # Mark the parking lot as unavailable
                parking_lot.availability = False
                parking_lot.save()

                print(f"Booking saved: {booking}")

                # Redirect to the PDF generation view
                return redirect('generate_parking_pdf', booking_id=booking.id)
            else:
                return render(request, 'website/ticket.html', {
                    'event': event,
                    'tickets': tickets,
                    'parking_lots': parking_lots,
                    'error': 'The selected parking lot is no longer available.'
                })
        else:
            return render(request, 'website/ticket.html', {
                'event': event,
                'tickets': tickets,
                'parking_lots': parking_lots,
                'error': 'All fields are required.'
            })
    
    context = {
        'event': event,
        'tickets': tickets,
        'parking_lots': parking_lots
    }
    return render(request, 'website/ticket.html', context)


def checkout_view(request, ticket_id):
    # Fetch the ticket based on ticket_id
    ticket = get_object_or_404(Ticket, id=ticket_id)
    event = ticket.event

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save the form instance without committing to add the ticket association
            checkout = form.save(commit=False)
            checkout.ticket = ticket
            checkout.event = event
            checkout.purchased_ticket = ticket  # Ensure this field is set
            checkout.save()

            # Redirect to the generate_pdf view after saving
            return redirect('generate_pdf', checkout_id=checkout.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = CheckoutForm()

    return render(request, 'website/checkout.html', {'form': form, 'ticket': ticket, 'event':event})

def generate_pdf_with_qr(request, checkout_id):
    # Fetch checkout data and related event data from your models
    checkout = get_object_or_404(Checkout, id=checkout_id)
    event = checkout.event  # Replace with the actual related event field if needed
    ticket_name = checkout.purchased_ticket.name
    
    qr_code_url = request.build_absolute_uri(checkout.qr_code.url)
    event_banner_url = request.build_absolute_uri(event.banner.url)
    
    # Render the HTML template with context including checkout and event
    context = {
        'checkout': checkout,
        'event': event,
        'ticket_name':ticket_name,
        'qr_code_url': qr_code_url,
        'event_banner_url': event_banner_url
        # Ensure event details are included if needed
    }
    html_content = render_to_string('website/ticket_template.html', context)
    
    # Write the HTML content to a temporary file
    temp_html_path = 'temp_ticket.html'
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Generate the PDF using wkhtmltopdf and save it to a temporary file
    output_pdf_path = 'output_ticket.pdf'
    subprocess.run([
    'C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe',
    '--enable-local-file-access',
    '--no-stop-slow-scripts',
    temp_html_path,
    output_pdf_path
    ], check=True)

    
    # Send the generated PDF as a response
    with open(output_pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="ticket.pdf"'
        return response


def send_ticket_with_pdf(checkout):
    # Create PDF buffer as above
    buffer = BytesIO()
    generate_pdf_with_qr(checkout.id).write(buffer)

    # Prepare the email
    email = EmailMessage(
        'Your Event Ticket',
        'Dear Customer, please find your event ticket attached.',
        'from@example.com',
        [checkout.email],
    )
    email.attach(f'ticket_{checkout.ticket_id}.pdf', buffer.getvalue(), 'application/pdf')
    email.send()
    
    
#_____________________________ contact form______________________________
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully. We will get back to you shortly!')
            return redirect('contact')  # Redirect to the same page or a success page
    else:
        form = ContactForm()
    
    return render(request, 'website/contact_form.html', {'form': form})


def about(request):
    return render(request, 'website/about.html',{})
        
        
 
def become_sponsor(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        logo = request.FILES.get('logo')
        telephone = request.POST.get('telephone')

        # Create a new sponsor instance and save it to the database
        Sponsor.objects.create(
            company_name=company_name,
            logo=logo,
            telephone=telephone,
            paid=False
        )
        return redirect('Home')

    # Render the form in the template
    return render(request, 'website/index.html')




def generate_parking_pdf(request, booking_id):
    booking = get_object_or_404(ParkingBooking, id=booking_id)
    parking_lot = booking.parking_lot
    event = parking_lot.event
    
    qr_code_url = request.build_absolute_uri(booking.qr_code.url)
    car_image_url = request.build_absolute_uri(static('images/icons/car.png'))

    context = {
        'booking': booking,
        'parking_lot': parking_lot,
        'event': event,
        'qr_code_url':qr_code_url,
        'car_image_url':car_image_url
    }

    html_content = render_to_string('website/parking_ticket_template.html', context)

    temp_html_path = 'temp_parking_ticket.html'
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    output_pdf_path = 'output_parking_ticket.pdf'
    subprocess.run([
        'C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe',
        '--enable-local-file-access',
        '--no-stop-slow-scripts',
        temp_html_path,
        output_pdf_path
    ], check=True)

    with open(output_pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="parking_ticket.pdf"'
        return response
    
    
    
    

def register_performer(request):
    if request.method == 'POST':
        form = PerfomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please wait for approval.')
            return redirect('perfomers')
        else:
            messages.error(request, 'There was an error with your submission.')
    return redirect('perfomers')    



# class PerformerLoginView(View):
#     # Redirect any GET requests back to the homepage or another appropriate page
#     def get(self, request):
#         return redirect('/')  # Redirect to homepage or any preferred page

#     def post(self, request):
#         email = request.POST.get('email')
#         security_code = request.POST.get('security_code')
        
#         if not email or not security_code:
#             messages.error(request, 'Email and security code are required.')
#             return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect back to the page with the modal

#         try:
#             performer = Perfomer.objects.get(email=email, security_code=security_code)
#             request.session['performer_id'] = performer.id
#             messages.success(request, 'Login successful!')
#             return redirect('performer_dashboard') 
#         except Perfomer.DoesNotExist:
#             messages.error(request, 'Invalid email or security code.')
#             return redirect(request.META.get('HTTP_REFERER', '/'))





class PerformerLoginView(View):
    def get(self, request):
        """Handles GET request and initializes an empty form."""
        form = PerformerLoginForm()
        return render(request, 'website/index.html', {'form': form})

    def post(self, request):
        """Handles POST request for login form submission."""
        form = PerformerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            security_code = form.cleaned_data['security_code']

            # Check if the performer exists
            try:
                performer = Perfomer.objects.get(email=email, security_code=security_code)
                # Store performer ID in session
                request.session['performer_id'] = performer.id
                messages.success(request, 'Login successful!')
                return redirect('performer_dashboard')
            except Perfomer.DoesNotExist:
                form.add_error(None, 'Invalid email or security code.')

        # If form is not valid or performer doesn't exist, return form with errors
        return render(request, 'website/index.html', {'form': form})




        
        

class PerformerDashboardView(View):
    def get(self, request):
        # Get the performer ID from the session
        performer_id = request.session.get('performer_id')
        if not performer_id:
            # Redirect to the login modal if the performer is not logged in
            return HttpResponse('Invalid email or security code, try again later!')

        try:
            # Retrieve the performer using the ID from the session
            performer = Perfomer.objects.get(id=performer_id)
        except Perfomer.DoesNotExist:
            # Clear session if performer no longer exists, then redirect to login
            request.session.flush()
            return HttpResponse('Invalid email or security code, try again later!')

        # Fetch all invitations related to the performer
        invitations = performer.invitations.all()

        # Render the dashboard template with performer and invitations
        return render(request, 'website/performer_dashboard.html', {
            'performer': performer,
            'invitations': invitations
        })

    
    
def logout_performer(request):
    # Clear the session data for the performer
    request.session.flush()  # This clears all session data
    return redirect('Home')  # Redirect to home or login page      


def approve_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    invitation.status = 'approved'
    invitation.save()
    return redirect('performer_dashboard')  # Adjust as needed

def reject_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    invitation.status = 'rejected'
    invitation.save()
    return redirect('performer_dashboard')  # Adjust as needed      