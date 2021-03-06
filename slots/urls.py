from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('api/slots/', views.SlotView.as_view(), name="slots"),
    path('api/bookings/', views.BookingView.as_view(), name="bookings"),
    path('api/adminbookings/', views.AdminBookingView.as_view(), name="adminbookings"),
    path('api/activate/', views.slotActivate, name="activate"),
    path('api/deactivate/', views.slotDeactivate, name="deactivate"),
    path('api/reqcancel/', views.reqCancelBooking, name="reqcancel"),
    path('api/rescancel/', views.resCancelBooking, name="rescancel"),
    path('api/completed/', views.markCompleted, name="completed"),
]
