from rest_framework import serializers
from .models import Slots, Bookings


class SlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'


class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
