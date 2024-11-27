from django.contrib import admin
from base.models import Category, Ticket, Event, Perfomer, Checkout, Invitation, Sponsor, Video, ParkingLot, ParkingBooking, Notification
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Contact

class PerfomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','gender','description','category','img_tag']
    
    def img_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "No image"
    
class EventAdmin(admin.ModelAdmin):
    list_display = ['name','location','date','description','img_tag']
    
    def img_tag(self, obj):
        if obj.banner:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.banner.url))    
        return "No image"
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name','event', 'price','number_of_ticket',)

  
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['firstname','lastname','email','phonenumber','ticket_id','qr_code_img','payment_method']

    def qr_code_img(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.qr_code.url))
        return "No QR Code"

    qr_code_img.short_description = "QR Code Preview"
    

class InvitationAdmin(admin.ModelAdmin):
    list_display = ['performer','name','telephone','email','message','created_at']    
    
    
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['company_name','telephone','paid','logo_tag']
    
    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.logo.url))    
        return "No logo"     
    
class ParkingBookingAdmin(admin.ModelAdmin):
    list_display = ['parking_lot','firstname','lastname','telephone','payment_method','booked_at','qr_code_img']

    def qr_code_img(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.qr_code.url))
        return "No QR Code"

    qr_code_img.short_description = "QR Code Preview"      
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp']    
           
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Perfomer, PerfomerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category)
admin.site.register(Ticket,TicketAdmin)  
admin.site.register(Sponsor, SponsorAdmin)   
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Video)
admin.site.register(ParkingLot)
admin.site.register(ParkingBooking, ParkingBookingAdmin)
admin.site.register(Notification, NotificationAdmin)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email','message', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at',)
