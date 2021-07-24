from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Slots, Bookings
from rest_framework.response import Response
from .serializers import SlotsSerializer, BookingsSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view


# landing page
def home(request):
    return HttpResponse("Hospital Slot Booking System API")


# get and create slot
class SlotView(APIView):

    def get(self, request, *args, **kwargs):
        slots = Slots.objects.all()
        serializer = SlotsSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SlotsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get and create bookings
class BookingView(APIView):

    def get(self, request, *args, **kwargs):
        bookings = Bookings.objects.all()
        serializer = BookingsSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        slotId = request.data.get('slotId')
        slot = Slots.objects.get(id=slotId)

        if slot.isActive:

            if slot.isBooked:
                return Response('This slot is already booked.', status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer = BookingsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    slot.isBooked = True
                    slot.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    print('error', serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response('This slot is not available for booking yet.', status=status.HTTP_400_BAD_REQUEST)


# activate slot
@csrf_exempt
@api_view(['POST'])
def slotActivate(request):
    data = json.loads(request.body)
    slotId = data['slotId']
    slot = Slots.objects.get(id=slotId)

    if slot.isActive:
        return Response('This slot is already active.', status=status.HTTP_400_BAD_REQUEST)

    else:
        slot.isActive = True
        slot.save()
        return Response('Slot is activated.', status=status.HTTP_201_CREATED)


# deactivate slot
@csrf_exempt
@api_view(['POST'])
def slotDeactivate(request):
    data = json.loads(request.body)
    slotId = data['slotId']
    slot = Slots.objects.get(id=slotId)

    if slot.isActive:
        if slot.isBooked:
            return Response('This slot is booked. You need to cancel the appointment first to deactivate the slot.', status=status.HTTP_400_BAD_REQUEST)

        else:
            slot.isActive = False
            slot.save()
            return Response('Slot is deactivated.', status=status.HTTP_201_CREATED)

    else:
        return Response('This slot is already deactivated.', status=status.HTTP_400_BAD_REQUEST)


# cancel booking
@csrf_exempt
@api_view(['POST'])
def cancelBooking(request):
    data = json.loads(request.body)
    bookingId = data['id']
    booking = Bookings.objects.get(id=bookingId)

    if booking:
        if booking.isCompleted:
            return Response('This booking cannot be cancelled as it is already completed.', status=status.HTTP_400_BAD_REQUEST)

        else:
            if booking.isCancelled:
                return Response('This booking is already cancelled.', status=status.HTTP_400_BAD_REQUEST)

            else:
                booking.isCancelled = True
                booking.save()
                return Response('Booking Cancelled.', status=status.HTTP_201_CREATED)

    else:
        return Response('Booking does not exist.', status=status.HTTP_400_BAD_REQUEST)
