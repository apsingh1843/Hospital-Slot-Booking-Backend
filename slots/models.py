from django.db import models
import uuid
from django.contrib.auth.models import User


class Slots(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    startTime = models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    endTime = models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    isBooked = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['startTime']


class Bookings(models.Model):

    REQUEST_CHOICES = (
        ('NO', 'Not Requested'),
        ('RE', 'Requested'),
        ('AC', 'Accepted'),
        ('DE', 'Declined'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slotId = models.CharField(max_length=1000, blank=False, null=False)
    slotName = models.CharField(max_length=50, null=True)
    slotTime = models.CharField(max_length=200, null=True)
    bookedBy = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE, null=True)
    patientName = models.CharField(max_length=100, blank=False, null=False)
    bearerName = models.CharField(max_length=100, blank=False, null=False)
    patientAge = models.IntegerField(null=False, blank=False)
    mobile = models.IntegerField(null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    bookingTime = models.DateTimeField(auto_now_add=True)
    isCompleted = models.BooleanField(default=False)
    requestCancel = models.CharField(max_length=50, choices=REQUEST_CHOICES, default='NO')
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.patientName)

    class Meta:
        ordering = ['-bookingTime']
