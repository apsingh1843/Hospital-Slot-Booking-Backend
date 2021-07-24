from django.db import models
import uuid


class Slots(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    startTime = models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    endTime = models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    isBooked = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
