from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid
from django.utils.timezone import now, localtime
from django.core.files.storage import FileSystemStorage
from django.db import models
import pytz

def create_rand_id():
        from django.utils.crypto import get_random_string
        return get_random_string(length=13, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    verification_code = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_first_time = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EventPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_number = models.IntegerField()
    name = models.CharField(max_length=255)
    is_reserved = models.BooleanField(default=False)
    is_occupied = models.BooleanField(default=False)
    reservation_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {str(self.room_number)}"
    
    def get_room_number(self):
        return self.room_number
    
    def get_local_end_time(self):
        """ Get start_time in Asia/Manila timezone without saving """
        manila_tz = pytz.timezone('Asia/Manila')
        return self.reservation_end_time.astimezone(manila_tz) if self.reservation_end_time else None

    class Meta:
        verbose_name_plural = "Events Places"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done')
    ]

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(EventPlace, on_delete=models.CASCADE)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def get_local_start_time(self):
        """ Get start_time in Asia/Manila timezone without saving """
        manila_tz = pytz.timezone('Asia/Manila')
        return self.start_time.astimezone(manila_tz) if self.start_time else None

    def get_local_end_time(self):
        """ Get end_time in Asia/Manila timezone without saving """
        manila_tz = pytz.timezone('Asia/Manila')
        return self.end_time.astimezone(manila_tz) if self.end_time else None
    
    def update_status(self):
        """ Update the status based on the current time """
        current_time = now()
        if self.start_time <= current_time < self.end_time:
            self.status = 'parked'
        elif current_time >= self.end_time:
            self.status = 'expired'
        self.save()

    def __str__(self):
        return str(self.user) + " " + str(self.room) + " " + str(self.start_time) + " " + str(self.end_time)
    
        
    class Meta:
        verbose_name_plural = "Reservations"
        ordering = ['-start_time']

