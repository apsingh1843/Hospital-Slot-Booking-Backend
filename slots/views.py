from django.http import HttpResponse
from .models import Slots, Bookings
from rest_framework.response import Response
from .serializers import SlotsSerializer, BookingsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes


# landing page
def home(request):
    return HttpResponse("Hospital Slot Booking System API")


# get and create slot
class SlotView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

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
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_staff:
            bookings = Bookings.objects.all()
        else:
            bookings = self.request.user.bookings.all()

        serializer = BookingsSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        slotId = request.data.get('slotId')
        slot = Slots.objects.get(id=slotId)

        if slot.isActive:

            if slot.isBooked:
                return Response({'msg': 'This slot is already booked.'},
                status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer = BookingsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    slot.isBooked = True
                    slot.save()
                    return Response({'msg': 'Successfully booked slot.'},
                    status=status.HTTP_201_CREATED)
                else:
                    print('error', serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'msg': 'This slot is not available for booking yet.'},
            status=status.HTTP_400_BAD_REQUEST)


# activate slot
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
def slotActivate(request):
    data = json.loads(request.body)
    slotId = data['slotId']
    slot = Slots.objects.get(id=slotId)

    if slot.isActive:
        return Response({'msg': 'This slot is already active.'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        slot.isActive = True
        slot.save()
        return Response({'msg': 'Slot is activated.'}, status=status.HTTP_200_OK)


# deactivate slot
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
def slotDeactivate(request):
    data = json.loads(request.body)
    slotId = data['slotId']
    slot = Slots.objects.get(id=slotId)

    if slot.isActive:
        if slot.isBooked:
            return Response({'msg': 'This slot is booked. You need to cancel the appointment first to deactivate the slot.'},
            status=status.HTTP_400_BAD_REQUEST)

        else:
            slot.isActive = False
            slot.save()
            return Response({'msg': 'Slot is deactivated.'}, status=status.HTTP_200_OK)

    else:
        return Response({'msg': 'This slot is already deactivated.'}, status=status.HTTP_400_BAD_REQUEST)


# request cancel booking
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reqCancelBooking(request):
    data = json.loads(request.body)
    bookingId = data['id']
    reqMsg = data['reqMsg']

    booking = Bookings.objects.get(id=bookingId)

    if booking:
        if booking.isCompleted:
            return Response({'msg': 'This booking cannot be cancelled as it is already completed.'},
            status=status.HTTP_400_BAD_REQUEST)

        else:
            if booking.requestCancel == 'AC':
                return Response({'msg': 'This booking is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST)

            elif booking.requestCancel == 'DE':
                return Response({'msg': 'Your request for cancelling this booking was declined earlier.'},
                status=status.HTTP_400_BAD_REQUEST)

            elif booking.requestCancel == 'RE':
                return Response({'msg': 'You have already requested earlier.Please wait for response.'},
                status=status.HTTP_400_BAD_REQUEST)

            else:
                booking.requestCancel = 'RE'
                booking.message = reqMsg
                booking.save()
                return Response({'msg': 'Request for cancelling this booking is sent.'},
                status=status.HTTP_200_OK)

    else:
        return Response({'msg': 'Booking does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


# response cancel booking
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
def resCancelBooking(request):
    data = json.loads(request.body)
    bookingId = data['id']
    resType = data['resType']
    resMsg = data['resMsg']

    booking = Bookings.objects.get(id=bookingId)
    slotId = booking.slotId
    slot = Slots.objects.get(id=slotId)

    if booking:
        if booking.isCompleted:
            return Response({'msg': 'This booking is already completed.'},
            status=status.HTTP_400_BAD_REQUEST)

        else:
            booking.requestCancel = resType

            if resType == 'AC':
                booking.isCompleted = True
                slot.isBooked = False
                slot.isActive = False

            if resType == 'DE':
                booking.message = resMsg

            booking.save()
            slot.save()
            return Response({'msg': 'Response sent.'}, status=status.HTTP_200_OK)

    else:
        return Response({'msg': 'Booking does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


# mark booking as completed
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
def markCompleted(request):
    data = json.loads(request.body)
    bookingId = data['id']

    booking = Bookings.objects.get(id=bookingId)
    slotId = booking.slotId
    slot = Slots.objects.get(id=slotId)

    if booking:
        if booking.isCompleted:
            return Response({'msg': 'This booking is already completed.'},
            status=status.HTTP_400_BAD_REQUEST)

        else:
            booking.isCompleted = True
            slot.isActive = False
            slot.isBooked = False

            booking.save()
            slot.save()
            return Response({'msg': 'Response sent.'}, status=status.HTTP_200_OK)

    else:
        return Response({'msg': 'Booking does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
