from django.urls import path
from base import views

urlpatterns = [
    path('', views.home, name="Home"),
    path("details/<int:id>/", views.perfomerdetails, name='details'),
    path("perfomers/", views.perfomers, name='perfomers'),
    path('invite-performer/<int:id>/', views.invite_performer, name='invite_performer'),
    path('events/', views.Events, name="events"),
    path('ticket/<int:event_id>/', views.Tickets, name="ticket"),
    path('checkout/<int:ticket_id>/', views.checkout_view, name='checkout'),
    path('checkout/<int:checkout_id>/generate-pdf/', views.generate_pdf_with_qr, name='generate_pdf'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about, name='about'),
    path('become-sponsor/', views.become_sponsor, name='become_sponsor'),
    path('generate-parking-pdf/<int:booking_id>/', views.generate_parking_pdf, name='generate_parking_pdf'),
    path('register-performer/', views.register_performer, name='register_performer'),
    # path('performer/login/', views.PerformerLoginView.as_view(), name='performer_login'),
    path('performer-login/', views.PerformerLoginView.as_view(), name='performer_login'),
    path('performer-dashboard', views.PerformerDashboardView.as_view(), name='performer_dashboard'),
    path('logout/', views.logout_performer, name='logout'),
]
