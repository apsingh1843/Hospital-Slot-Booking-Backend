from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('api/slots/', views.SlotView.as_view(), name="slots"),
    path('api/bookings/', views.BookingView.as_view(), name="bookings"),
    path('api/activate/', views.slotActivate, name="activate"),
    path('api/deactivate/', views.slotDeactivate, name="deactivate"),
    path('api/cancel/', views.cancelBooking, name="cancel"),
]
