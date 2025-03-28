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


class Extracurricular(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    time = models.TimeField()
    duration = models.DurationField()
    is_active = models.BooleanField(default=True)

    
    class Meta:
        verbose_name_plural = "Extracurriculars"

    def __str__(self):
        return f"{self.name} {self.start_date} {self.end_date} {self.time} {self.duration}"